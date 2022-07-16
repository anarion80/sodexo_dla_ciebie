"""
Custom integration to integrate Sodexo Dla Ciebie with Home Assistant.

For more details about this integration, please refer to
https://github.com/anarion80/sodexo_dla_ciebie
"""
import asyncio
from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config, HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from homeassistant.const import (
    CONF_PASSWORD,
    CONF_USERNAME,
)

from .api import SodexoApiClient

from .const import (
    DOMAIN,
    PLATFORM,
    STARTUP_MESSAGE,
)

SCAN_INTERVAL = timedelta(minutes=30)

_LOGGER = logging.getLogger(__package__)


async def async_setup(hass: HomeAssistant, config: Config) -> bool:
    """Set up this integration using YAML is not supported."""
    # pylint: disable=unused-argument
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.info(STARTUP_MESSAGE)

    hass_data = dict(entry.data)
    hass.data[DOMAIN][entry.entry_id] = hass_data
    # Forward the setup to the sensor platform.
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, PLATFORM)
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    unloaded = all(
        await asyncio.gather(
            *[hass.config_entries.async_forward_entry_unload(entry, PLATFORM)]
        )
    )
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
