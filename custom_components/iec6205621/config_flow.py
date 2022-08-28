"""Config flow for iec6205621 integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from .iec6205621 import IEC6205621, iecError

from homeassistant.config_entries import ConfigFlow
from homeassistant.const import CONF_DEVICE
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_DEVICE): str,
})

class IECConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for iec6205621."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            try:
                api = IEC6205621(user_input[CONF_DEVICE],_LOGGER)
                await self.hass.async_add_executor_job(api.update)
            except (iecError):
                _LOGGER.exception("Cannot connect to electricity meter")
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(
                    title="Electricity meter",
                    data={
                        CONF_DEVICE: user_input[CONF_DEVICE],
                    },
                )

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )
