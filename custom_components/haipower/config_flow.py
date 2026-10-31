"""Config flow for HaiPower Solar & Battery integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from . import HaiPowerDataUpdateCoordinator
from .const import DEFAULT_BASE_URL, DOMAIN, SERVER_URLS

_LOGGER = logging.getLogger(__name__)


class HaiPowerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for HaiPower Solar & Battery."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            username = user_input["username"].strip()
            password = user_input["password"]
            dsn = user_input.get("dsn", "").strip()
            base_url = user_input.get("base_url", DEFAULT_BASE_URL)

            session = async_get_clientsession(self.hass)
            coordinator = HaiPowerDataUpdateCoordinator(
                self.hass, username, password, dsn, base_url
            )

            try:
                info = await coordinator.async_discover_device(session)
                discovered_dsn = info["dsn"]
                station_name = info["station_name"]
            except Exception as err:  # noqa: BLE001
                _LOGGER.error("HaiPower setup validation error: %s", err)
                errors["base"] = "invalid_auth"
            else:
                await self.async_set_unique_id(f"haipower_{discovered_dsn}")
                self._abort_if_unique_id_configured()

                save_data = {
                    "username": username,
                    "password": password,
                    "dsn": discovered_dsn,
                    "base_url": base_url,
                }
                return self.async_create_entry(
                    title=f"HaiPower Solar ({station_name})",
                    data=save_data,
                )

        schema = vol.Schema(
            {
                vol.Required("username"): str,
                vol.Required("password"): str,
                vol.Optional("base_url", default=DEFAULT_BASE_URL): vol.In(SERVER_URLS),
                vol.Optional("dsn", default=""): str,
            }
        )
        return self.async_show_form(
            step_id="user", data_schema=schema, errors=errors
        )
