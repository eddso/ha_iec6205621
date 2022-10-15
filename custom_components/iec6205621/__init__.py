"""The iec6205621 component."""
from datetime import timedelta
import logging

from .iec6205621 import IEC6205621, iecError

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_DEVICE, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN

PLATFORMS = [Platform.SENSOR]

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up iec6205621 from a config entry."""
    api = IEC6205621(entry.data[CONF_DEVICE], _LOGGER)

    try:
       await hass.async_add_executor_job(api.update)
    except iecError as exception:
       raise ConfigEntryNotReady from exception

    async def async_update_data():
        """Fetch data from the API."""
        try:
            await hass.async_add_executor_job(api.update)
        except iecError as exception:
            pass
        return api

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="iec6205621",
        update_method=async_update_data,
        update_interval=timedelta(seconds=300),
    )

    # await coordinator.async_config_entry_first_refresh()
    await coordinator.async_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # hass version 2022.8+
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    #hass.config_entries.async_setup_platforms(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
