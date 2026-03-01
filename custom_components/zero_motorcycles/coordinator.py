"""DataUpdateCoordinator."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from custom_components.zero_motorcycles.models import ZeroBikeData

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant



"""DataUpdateCoordinator for Zero Motorcycle."""
from datetime import timedelta

from .api import ZeroApiClient
from .const import DOMAIN, LOGGER


class ZeroDataCoordinator(DataUpdateCoordinator[ZeroBikeData]):
    """Class to manage fetching Zero Motorcycle data."""

    def __init__(
        self,
        hass: HomeAssistant,
        api_client: ZeroApiClient,
    ) -> None:
        """Initialize."""
        self.api_client = api_client
        self.unit_number = None

        super().__init__(
            hass,
            LOGGER,
            name=DOMAIN,
            # Community recommendation: 2-5 minutes to avoid API lockout
            update_interval=timedelta(minutes=10),
        )

    async def _async_update_data(self) -> ZeroBikeData:
        """Update data via library."""
        try:
            # 1. Ensure we have the unit number (only fetch once)
            if not self.unit_number:
                self.unit_number = await self.api_client.get_unit_number()

            # 2. Fetch the raw JSON list
            result = await self.api_client.get_bike_data(self.unit_number)
        except Exception as err:
            raise UpdateFailed(f"Error communicating with Zero API: {err}") from err
        else:
            LOGGER.debug("Fetched raw bike data: %s", result)
            return result
