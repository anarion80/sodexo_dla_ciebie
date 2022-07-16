"""Sample API Client."""
import json
import logging
import asyncio
import aiohttp
import async_timeout


# import socket

from .const import API_URL, LOGIN_URL

TIMEOUT = 10

_LOGGER = logging.getLogger(__package__)

HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}


class SodexoApiClient:
    """Interfaces to https://api4you.sodexo.pl/"""

    def __init__(
        self, username: str, password: str, session: aiohttp.ClientSession
    ) -> None:
        """Sodexo API Client."""
        self._username = username
        self._password = password
        self._session = session

    async def login(self):
        """Issue LOGIN request."""
        try:
            async with async_timeout.timeout(TIMEOUT):
                async with self._session.post(
                    LOGIN_URL,
                    data=json.dumps(
                        {"login": self._username, "password": self._password}
                    ),
                    headers=HEADERS,
                ) as res:
                    if res.status == 200 and res.content_type == "application/json":
                        resp = await res.json()
                        if resp["token"]:
                            token = resp["token"]
                            _LOGGER.debug("Got token!")
                            return token
                        raise Exception("Login failed!", resp["message"])
                    raise Exception("Could not retrieve token for user, login failed")
        except aiohttp.ClientError as err:
            _LOGGER.exception(err)

        except asyncio.TimeoutError as exception:
            _LOGGER.error(
                "Timeout error fetching information from %s - %s",
                LOGIN_URL,
                exception,
            )

        # except (KeyError, TypeError) as exception:
        #     _LOGGER.error(
        #         "Error parsing information from %s - %s",
        #         LOGIN_URL,
        #         exception,
        #     )
        # except (aiohttp.ClientError, socket.gaierror) as exception:
        #     _LOGGER.error(
        #         "Error fetching information from %s - %s",
        #         LOGIN_URL,
        #         exception,
        #     )
        # except Exception as exception:  # pylint: disable=broad-except
        #     _LOGGER.error("Something really wrong happened! - %s", exception)

    async def get_cards(self, token: str) -> json:
        """Get all cards"""
        try:
            _LOGGER.debug("Getting all cards...")
            _LOGGER.debug("Token: %s", token)

            async with self._session.get(
                API_URL,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Authorization": token,
                },
            ) as res:
                if res.status == 200 and res.content_type == "application/json":
                    resp = await res.json()
                    return resp
                raise Exception("Could not retrieve account information from API")
        except aiohttp.ClientError as err:
            _LOGGER.exception(err)

    async def get_card_details(self, token: str, card_id: int) -> json:
        """Get single card data"""
        try:
            _LOGGER.debug("Getting card details...")
            _LOGGER.debug("Token: %s", token)
            async with self._session.get(
                f"{API_URL}/{card_id}",
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Authorization": token,
                },
            ) as res:
                if res.status == 200 and res.content_type == "application/json":
                    card = await res.json()
                    return card
                raise Exception("Could not retrieve card information from API")
        except aiohttp.ClientError as err:
            _LOGGER.exception(err)
