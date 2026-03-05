"""
Zero Motorcycles unofficial API client.

This client implements a small, resilient wrapper around the
unofficial Zero Motorcycles REST API. It performs authentication,
fetches vehicle list and per-vehicle status information. The exact
endpoints used can be overridden with `base_url` for testing.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import aiohttp
import async_timeout

from custom_components.zero_motorcycles.const import LOGGER
from custom_components.zero_motorcycles.parser import ZeroParser

if TYPE_CHECKING:
    from custom_components.zero_motorcycles.models import ZeroBikeData


class ZeroApiClientError(Exception):
    """Exception to indicate a general API error."""


class ZeroApiClientCommunicationError(ZeroApiClientError):
    """Exception to indicate a communication error."""


class ZeroApiClientAuthenticationError(ZeroApiClientError):
    """Exception to indicate an authentication error."""


class ZeroApiClient:
    """ApiClient for Zero Motorcycle Mongol API."""

    def __init__(self, username: str, password: str, session: aiohttp.ClientSession):
        self._username = username
        self._password = password
        self._session = session
        self._base_url = "https://mongol.brono.com/mongol/api.php"

    def _verify_response_or_raise(self, response: aiohttp.ClientResponse) -> None:
        """Verify that the response is valid and raise appropriate errors."""
        if response.status in (401, 403):
            raise ZeroApiClientAuthenticationError
        try:
            response.raise_for_status()
        except aiohttp.ClientResponseError as err:
            error_msg = f"Unexpected response: {err}"
            raise ZeroApiClientError(error_msg) from err

    async def get_unit_number(self) -> str | None:
        """Fetch the unit number (ID) of your motorcycle."""
        params = {
            "commandname": "get_units",
            "format": "json",
            "user": self._username,
            "pass": self._password,
        }

        try:
            async with async_timeout.timeout(10):
                response = await self._session.get(self._base_url, params=params)
                self._verify_response_or_raise(response)
                data = await response.json()
                # Zero returns a list of units; we grab the first one
                if data and len(data) > 0:
                    return data[0]["unitnumber"]
                return None
        except Exception as e:
            error_msg = f"Error fetching unit number: {e}"
            raise ZeroApiClientError(error_msg) from e

    async def get_bike_data(self, unit_number: str) -> ZeroBikeData:
        """Fetch the latest telemetry data for a specific bike."""
        params = {
            "commandname": "get_last_transmit",
            "format": "json",
            "user": self._username,
            "pass": self._password,
            "unitnumber": unit_number,
        }

        try:
            async with async_timeout.timeout(10):
                response = await self._session.get(self._base_url, params=params)
                self._verify_response_or_raise(response)
                data = await response.json()
                LOGGER.debug("Raw API response for bike data: %s", data)
                return ZeroParser.parse_telemetry(data)
        except Exception as e:
            error_msg = f"Error communicating with Zero API: {e}"
            raise ZeroApiClientError(error_msg) from e
