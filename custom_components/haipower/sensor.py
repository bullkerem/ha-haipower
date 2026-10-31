"""Sensor platform for HaiPower Solar & Battery integration."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfPower,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import HaiPowerDataUpdateCoordinator
from .const import DOMAIN


@dataclass(frozen=True)
class HaiPowerSensorEntityDescription(SensorEntityDescription):
    """Describes HaiPower sensor entity."""

    api_key: str = ""
    scale: float = 1.0


SENSOR_TYPES: tuple[HaiPowerSensorEntityDescription, ...] = (
    # --- SOLAR PV PRODUCTION ---
    HaiPowerSensorEntityDescription(
        key="solar_power",
        name="Güneş Anlık Üretim",
        api_key="ppvAll",
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:solar-power-variant",
    ),
    HaiPowerSensorEntityDescription(
        key="solar_today",
        name="Güneş Günlük Üretim",
        api_key="epVAllToday",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:solar-panel-large",
    ),
    HaiPowerSensorEntityDescription(
        key="solar_month",
        name="Güneş Aylık Üretim",
        api_key="epvMonth",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:solar-panel",
    ),
    HaiPowerSensorEntityDescription(
        key="solar_year",
        name="Güneş Yıllık Üretim",
        api_key="epvYear",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:solar-power",
    ),
    HaiPowerSensorEntityDescription(
        key="solar_total",
        name="Güneş Toplam Üretim",
        api_key="epvTotal",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:White-balance-sunny",
    ),
    HaiPowerSensorEntityDescription(
        key="vpv1",
        name="PV1 Gerilim",
        api_key="vpv1",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:flash-triangle",
    ),
    HaiPowerSensorEntityDescription(
        key="vpv2",
        name="PV2 Gerilim",
        api_key="vpv2",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:flash-triangle",
    ),
    # --- BATTERY ---
    HaiPowerSensorEntityDescription(
        key="battery_soc",
        name="Batarya Doluluk (SOC)",
        api_key="soc",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery-high",
    ),
    HaiPowerSensorEntityDescription(
        key="battery_voltage",
        name="Batarya Gerilimi",
        api_key="vbat",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:car-battery",
    ),
    HaiPowerSensorEntityDescription(
        key="battery_charge_power",
        name="Batarya Anlık Şarj Gücü",
        api_key="pcharge",
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery-charging",
    ),
    HaiPowerSensorEntityDescription(
        key="battery_discharge_power",
        name="Batarya Anlık Deşarj Gücü",
        api_key="pdischarge",
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery-arrow-down",
    ),
    HaiPowerSensorEntityDescription(
        key="battery_charge_today",
        name="Batarya Günlük Şarj",
        api_key="echargeToday",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:battery-plus-variant",
    ),
    HaiPowerSensorEntityDescription(
        key="battery_discharge_today",
        name="Batarya Günlük Deşarj",
        api_key="edischargeToday",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:battery-minus-variant",
    ),
    # --- HOME LOAD / CONSUMPTION ---
    HaiPowerSensorEntityDescription(
        key="load_power",
        name="Ev Anlık Tüketim",
        api_key="plocalLoadtotal",
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:home-lightning-bolt",
    ),
    HaiPowerSensorEntityDescription(
        key="load_today",
        name="Ev Günlük Tüketim",
        api_key="eloadToday",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:home-analytics",
    ),
    HaiPowerSensorEntityDescription(
        key="load_month",
        name="Ev Aylık Tüketim",
        api_key="eloadMonth",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:home-clock",
    ),
    HaiPowerSensorEntityDescription(
        key="load_total",
        name="Ev Toplam Tüketim",
        api_key="eloadTotal",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:home-Import-outline",
    ),
    # --- GRID ---
    HaiPowerSensorEntityDescription(
        key="grid_import_power",
        name="Şebekeden Çekilen Anlık Güç",
        api_key="pactouserTotal",
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:transmission-tower-import",
    ),
    HaiPowerSensorEntityDescription(
        key="grid_export_power",
        name="Şebekeye Verilen Anlık Güç",
        api_key="pactogridtotal",
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:transmission-tower-export",
    ),
    HaiPowerSensorEntityDescription(
        key="grid_import_today",
        name="Şebekeden Günlük Çekilen Enerji",
        api_key="efromGridToday",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:transmission-tower",
    ),
    HaiPowerSensorEntityDescription(
        key="grid_export_today",
        name="Şebekeye Günlük Verilen Enerji",
        api_key="etoGridToday",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:transmission-tower-export",
    ),
    HaiPowerSensorEntityDescription(
        key="grid_import_total",
        name="Şebekeden Toplam Çekilen Enerji",
        api_key="efromGridTotal",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:transmission-tower",
    ),
    HaiPowerSensorEntityDescription(
        key="grid_export_total",
        name="Şebekeye Toplam Verilen Enerji",
        api_key="etoGridTotal",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:transmission-tower-export",
    ),
    # --- STATUS ---
    HaiPowerSensorEntityDescription(
        key="inverter_status",
        name="İnverter Durumu",
        api_key="status2",
        icon="mdi:check-network",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up HaiPower sensors based on a config entry."""
    coordinator: HaiPowerDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    entities = [
        HaiPowerSensor(coordinator, description) for description in SENSOR_TYPES
    ]
    async_add_entities(entities)


class HaiPowerSensor(
    CoordinatorEntity[HaiPowerDataUpdateCoordinator], SensorEntity
):
    """Representation of a HaiPower Sensor."""

    entity_description: HaiPowerSensorEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: HaiPowerDataUpdateCoordinator,
        description: HaiPowerSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"haipower_{coordinator.dsn}_{description.key}"

        station_name = coordinator.station_name or f"HaiPower ({coordinator.dsn})"
        model = coordinator.device_model or "Hybrid Inverter"
        rated_kw = (coordinator.data or {}).get("power")
        if rated_kw:
            model = f"{model} ({rated_kw} kW)"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.dsn)},
            name=f"HaiPower Solar ({station_name})",
            manufacturer="HaiPower / Aohai Digital Power",
            model=model,
            serial_number=coordinator.dsn,
            configuration_url=coordinator.base_url,
        )

    @property
    def native_value(self) -> Any:
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None
        val = self.coordinator.data.get(self.entity_description.api_key)
        if val is None:
            return None
        if self.entity_description.key == "inverter_status":
            status_map = {
                "OnGrid": "Şebekede Aktif (OnGrid)",
                "OffGrid": "Ada Modu (OffGrid)",
                "Wait": "Beklemede",
                "Fault": "Arıza",
            }
            return status_map.get(str(val), str(val))
        return val

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return extra attributes on the status sensor."""
        if self.entity_description.key != "inverter_status" or not self.coordinator.data:
            return None
        d = self.coordinator.data
        return {
            "station_name": d.get("_station_name") or self.coordinator.station_name,
            "dsn": d.get("dsn"),
            "csn": d.get("csn"),
            "last_update": d.get("lastTime"),
            "rated_power_kw": d.get("power"),
            "vac1": d.get("vac1"),
            "vac2": d.get("vac2"),
            "vac3": d.get("vac3"),
            "co2_saved_tons": d.get("co2Total"),
            "trees_planted": d.get("treeTotal"),
        }
