"""The sensor entity for the iec6205621 integration."""
from __future__ import annotations
import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_DEVICE, UnitOfEnergy
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Initialize the integration."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    device = entry.data[CONF_DEVICE]
    if (device := entry.data[CONF_DEVICE]) is None:
        device = entry.entry_id

    entities = []
    for sensor in coordinator.data.sensors:
        _LOGGER.debug("add sensor %s, %s", device, sensor)
        entities.append(OBISMeter(coordinator, device, sensor))
    async_add_entities(entities)


class OBISMeter(CoordinatorEntity, SensorEntity): 
    """Class for a sensor."""
    def __init__(self, coordinator, device, sensor):
        """Initialize an sensor."""
        super().__init__(coordinator)
        self._sensor = sensor
        self._device = device
        self._attr_unique_id = f"{DOMAIN}_{device}_{sensor}"
        self._attr_name = coordinator.data.sensors[sensor]['name']
        self._attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"{device}")},
            manufacturer=coordinator.data.manufacturer,
            model=coordinator.data.model,
            name=coordinator.data.model,
            sw_version=coordinator.data.firmware_version,
            hw_version=coordinator.data.serial_number,
        )

    @property
    def available(self):
        """Return if entity is available."""
        return self.coordinator.last_update_success

    @property
    def native_value(self):
        """Return the state of the sensor."""
        value = self.coordinator.data.sensors[self._sensor]['value']
        _LOGGER.debug("%s %f", self._sensor, value)
        
        return value
