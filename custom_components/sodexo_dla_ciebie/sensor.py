"""Sensor platform for Sodexo integration."""
from datetime import timedelta
import logging
from typing import Any, Dict

from aiohttp import ClientError

from homeassistant import config_entries, core
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.typing import StateType

from .api import SodexoApiClient
from .const import ACTIVE_ONLY, ATTRIBUTION, DEFAULT_ICON, DOMAIN, UNIT_OF_MEASUREMENT

_LOGGER = logging.getLogger(__package__)

SCAN_INTERVAL = timedelta(minutes=60)


async def async_setup_entry(
    hass: core.HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
):
    """Set up sensor platform."""
    _LOGGER.debug("Sensor: async_setup_entry")
    session = async_get_clientsession(hass, True)
    config = config_entry.data
    api = SodexoApiClient(config[CONF_USERNAME], config[CONF_PASSWORD], session)

    cards = []
    try:
        token = await api.login()
        if token:
            cards = await api.get_cards(token)
            _LOGGER.debug("Got %s card(s)", len(cards))
    except ClientError as err:
        _LOGGER.error("Error gettings cards from API - %s", err)

    sensors = []
    _LOGGER.debug("ACTIVE ONLY = %s", config[ACTIVE_ONLY])
    for card in cards:
        if config[ACTIVE_ONLY]:
            _LOGGER.debug("Only adding active cards")
            if card["status"] == "ACTIVE":
                _LOGGER.debug("Card %s is active - adding!", card["id"])
                sensors.append(SodexoCardSensor(api, card["id"], config))
        else:
            _LOGGER.debug("Adding card - regardless if it's active or not")
            sensors.append(SodexoCardSensor(api, card["id"], config))
    async_add_entities(sensors, update_before_add=True)


class SodexoCardSensor(SensorEntity):
    """Representation of a Sodexo Card (Sensor)."""

    def __init__(self, api: SodexoApiClient, _card_id: int, config: Any):
        """Init Sodexo card."""
        super().__init__()
        self._card_id = _card_id
        self._api = api
        self._config = config
        self._updated = None
        self._name = None

        self._icon = DEFAULT_ICON
        self._entity_picture = None
        self._unit_of_measurement = UNIT_OF_MEASUREMENT
        self._attr_native_unit_of_measurement = UNIT_OF_MEASUREMENT
        self._device_class = SensorDeviceClass.MONETARY
        self._state_class = SensorStateClass.TOTAL
        self._state = None
        self._available = False
        self.attrs: Dict[str, Any] = {}

    @property
    def name(self) -> str:
        """Return the name of the entity."""
        return self._name

    @property
    def has_entity_name(self) -> bool:
        """Return True if entity has a name."""
        return True

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return f"{DOMAIN}-{self._config[CONF_USERNAME]}-{self._card_id}".lower()

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._available

    @property
    def native_value(self) -> StateType:
        """Return the state."""
        return self._state

    @property
    def device_class(self):
        """Return device class."""
        return self._device_class

    @property
    def state_class(self):
        """Return state class."""
        return self._state_class

    @property
    def icon(self):
        """Return icon."""
        return self._icon

    @property
    def entity_picture(self):
        """Return Picture."""
        return self._entity_picture

    @property
    def attribution(self):
        """Return attribution."""
        return ATTRIBUTION

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return the state attributes."""
        attributes = {"updated": self._updated}
        attributes.update(self.attrs)
        return attributes

    @property
    def device_info(self) -> DeviceInfo:
        """Device info."""
        return DeviceInfo(
            default_name="Sodexo Dla Ciebie",
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN,)},  # type: ignore[arg-type]
            manufacturer="Sodexo Dla Ciebie",
            configuration_url="https://dlaciebie.sodexo.pl",
        )

    async def async_update(self) -> None:
        """Fetch new state and attributes data for the sensor."""
        api = self._api

        try:
            token = await api.login()
            if token:
                card = await api.get_card_details(token, self._card_id)
                self._state = card["balance"] / 100
                self._name = card["name"]
                self._updated = card["updateDateTime"]
                self._entity_picture = (
                    f"https://dlaciebie.sodexo.pl/static_img/{card['picture']}.png"
                )
                self.attrs["balanceLocked"] = card["balanceLocked"] / 100
                self.attrs["cardGroup"] = card["cardGroup"]
                self.attrs["creationDate"] = card["creationDT"]
                self.attrs["expiryDate"] = card["expiryDate"]
                self.attrs["id"] = card["cardDetails"]["id"]
                self.attrs["name"] = self._name
                self.attrs["number"] = card["number"]
                self.attrs["status"] = card["status"]
                self.attrs["totalNumOfTransactions"] = card["totalNumOfTransactions"]
                self._available = True
                _LOGGER.debug("Card %s updated from API", self._card_id)

        except ClientError as err:
            self._available = False
            _LOGGER.error("Error updating data from API - %s", err)
