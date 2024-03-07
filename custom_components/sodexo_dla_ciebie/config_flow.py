"""Adds config flow for Sodexo Card."""
import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.helpers.aiohttp_client import async_create_clientsession
import homeassistant.helpers.config_validation as cv

from .api import SodexoApiClient
from .const import ACTIVE_ONLY, DEFAULT_ACTIVE_ONLY, DOMAIN

_LOGGER = logging.getLogger(__package__)


class SodexoFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Sodexo."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        """Handle a flow initialized by the user."""
        _LOGGER.debug("Starting async_step_user...")
        self._errors = {}

        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_USERNAME].lower())
            self._abort_if_unique_id_configured()

            if await self._test_credentials(
                user_input[CONF_USERNAME], user_input[CONF_PASSWORD]
            ):
                _LOGGER.debug("Config is valid!")
                return self.async_create_entry(
                    title=user_input[CONF_USERNAME], data=user_input
                )
            self._errors = {"base": "auth"}

            return await self._show_config_form(user_input)

        user_input = {}
        # Provide defaults for form
        user_input[CONF_USERNAME] = ""
        user_input[CONF_PASSWORD] = ""
        user_input[ACTIVE_ONLY] = DEFAULT_ACTIVE_ONLY

        return await self._show_config_form(user_input)

    async def _show_config_form(self, user_input):  # pylint: disable=unused-argument
        """Show the configuration form to edit data."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_USERNAME, default=user_input[CONF_USERNAME]
                    ): cv.string,
                    vol.Required(
                        CONF_PASSWORD, default=user_input[CONF_PASSWORD]
                    ): cv.string,
                    vol.Required(
                        ACTIVE_ONLY, default=user_input[ACTIVE_ONLY]
                    ): cv.boolean,
                }
            ),
            errors=self._errors,
        )

    async def _test_credentials(self, username, password) -> bool:
        """Return true if credentials is valid."""
        try:
            session = async_create_clientsession(self.hass)
            client = SodexoApiClient(username, password, session)
            await client.login()
            return True
        except Exception as exception:  # pylint: disable=broad-except
            _LOGGER.error(exception)
            return False
