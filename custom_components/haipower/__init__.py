"""The HaiPower Solar & Battery integration (Aohai Digital Power Cloud)."""
from __future__ import annotations

from datetime import timedelta
import hashlib
import logging
import re
from typing import Any

import aiohttp

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DEFAULT_BASE_URL, DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]


class HaiPowerDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Class to manage fetching HaiPower cloud data."""

    def __init__(
        self,
        hass: HomeAssistant,
        username: str,
        password: str,
        dsn: str = "",
        base_url: str = DEFAULT_BASE_URL,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=60),
        )
        self.username = username.strip()
        self.password_md5 = hashlib.md5(password.encode("utf-8")).hexdigest().lower()
        self.dsn = dsn.strip()
        self.base_url = base_url.rstrip("/")
        self.token: str | None = None
        self.hid: int | None = None
        self.station_name: str | None = None
        self.device_model: str | None = None
        self.csn: str | None = None

    def _headers(self) -> dict[str, str]:
        """Return authenticated headers."""
        return {
            "Cookie": f"AUTH_USER_TOKEN={self.token}",
            "system_hid": str(self.hid),
            "Accept-Language": "en",
        }

    async def _async_login(self, session: aiohttp.ClientSession) -> None:
        """Authenticate with HaiPower / Aohai Cloud and extract JWT cookie."""
        url = f"{self.base_url}/auth/doWebLogin1"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Language": "en",
        }
        payload = {
            "code": "1",
            "userName": self.username,
            "password": self.password_md5,
        }
        async with session.post(url, data=payload, headers=headers, ssl=False, timeout=20) as resp:
            set_cookie = resp.headers.getall("Set-Cookie", [])
            cookie_str = "; ".join(set_cookie)
            match = re.search(r"AUTH_USER_TOKEN=([^;]+)", cookie_str)
            if match:
                self.token = match.group(1)
            body = await resp.json(content_type=None)
            if not body or body.get("code") != 200:
                msg = body.get("msg") if isinstance(body, dict) else "Unknown error"
                raise UpdateFailed(f"HaiPower login failed: {msg}")
            data = body.get("data") or {}
            self.hid = data.get("id")
            if not self.token:
                for cookie in session.cookie_jar:
                    if cookie.key == "AUTH_USER_TOKEN":
                        self.token = cookie.value
                        break
            if not self.token or not self.hid:
                raise UpdateFailed("HaiPower login succeeded but token/hid missing")

    async def async_discover_device(self, session: aiohttp.ClientSession) -> dict[str, Any]:
        """Discover station name and primary inverter DSN/CSN/model from the cloud account."""
        if not self.token or not self.hid:
            await self._async_login(session)

        # 1. Fetch Station list
        try:
            st_url = f"{self.base_url}/view/station/list?name=&offset=0&pageNum=1&pageSize=20"
            async with session.get(st_url, headers=self._headers(), ssl=False, timeout=20) as resp:
                st_body = await resp.json(content_type=None)
                if isinstance(st_body, dict) and st_body.get("code") == 200:
                    rows = (st_body.get("data") or {}).get("rows") or []
                    if rows:
                        self.station_name = rows[0].get("name") or "HaiPower Solar"
        except Exception as err:  # noqa: BLE001
            _LOGGER.debug("Station discovery warning: %s", err)

        # 2. Fetch Device list
        dev_url = f"{self.base_url}/view/device/list?csn=&dsn=&type=0&id=0&offset=0&pageNum=1&pageSize=20"
        async with session.get(dev_url, headers=self._headers(), ssl=False, timeout=20) as resp:
            dev_body = await resp.json(content_type=None)
            if not isinstance(dev_body, dict) or dev_body.get("code") != 200:
                raise UpdateFailed(f"Device list fetch failed: {dev_body}")
            rows = (dev_body.get("data") or {}).get("rows") or []
            if not rows:
                raise UpdateFailed("No inverter devices found on this HaiPower account")

            chosen = rows[0]
            if self.dsn:
                for row in rows:
                    if str(row.get("dsn", "")).strip() == self.dsn:
                        chosen = row
                        break

            self.dsn = str(chosen.get("dsn") or self.dsn).strip()
            self.csn = str(chosen.get("csn") or "").strip()
            self.device_model = str(chosen.get("typeName") or "Hybrid Inverter").strip()
            return {
                "dsn": self.dsn,
                "csn": self.csn,
                "model": self.device_model,
                "station_name": self.station_name or f"HaiPower ({self.dsn})",
            }

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch real-time inverter and energy data from HaiPower Cloud."""
        session = async_get_clientsession(self.hass)
        if not self.token or not self.hid:
            await self._async_login(session)
        if not self.dsn or not self.station_name or not self.device_model:
            await self.async_discover_device(session)

        url = f"{self.base_url}/view/data/deviceInfo?dsn={self.dsn}"
        async with session.get(url, headers=self._headers(), ssl=False, timeout=20) as resp:
            body = await resp.json(content_type=None)

        if not body or body.get("code") == 501 or body.get("code") != 200:
            # Re-login once if token expired
            await self._async_login(session)
            async with session.get(url, headers=self._headers(), ssl=False, timeout=20) as resp:
                body = await resp.json(content_type=None)

        if not body or body.get("code") != 200 or not body.get("data"):
            raise UpdateFailed(f"Error fetching HaiPower deviceInfo: {body}")

        data: dict[str, Any] = dict(body["data"])
        data["_station_name"] = self.station_name or f"HaiPower ({self.dsn})"
        data["_device_model"] = self.device_model or "Hybrid Inverter"
        return data


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up HaiPower from a config entry."""
    username = entry.data.get("username", "")
    password = entry.data.get("password", "")
    dsn = entry.data.get("dsn", "")
    base_url = entry.data.get("base_url", DEFAULT_BASE_URL)

    coordinator = HaiPowerDataUpdateCoordinator(hass, username, password, dsn, base_url)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
