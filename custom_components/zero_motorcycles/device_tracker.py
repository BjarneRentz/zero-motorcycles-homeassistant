from typing import TYPE_CHECKING

from homeassistant.components.device_tracker import SourceType, TrackerEntity

from custom_components.zero_motorcycles.coordinator import ZeroDataCoordinator

from .entity import ZeroMotorcycleEntity

if TYPE_CHECKING:
    from custom_components.zero_motorcycles.data import ZeroData


async def async_setup_entry(hass, entry, async_add_entities) -> None:  # noqa: ANN001, ARG001
    """Set up the Zero location tracker from a config entry."""
    # Assuming your entry.runtime_data holds the coordinator directly
    # or via a data object. Adjust according to your __init__.py logic.
    data: ZeroData = entry.runtime_data
    async_add_entities([ZeroMotorcycleTracker(data.coordinator)])


class ZeroMotorcycleTracker(ZeroMotorcycleEntity, TrackerEntity):
    """Representation of the motorcycle's location."""

    def __init__(self, coordinator: ZeroDataCoordinator):
        """Initialize the tracker."""
        # Match the base class: coordinator, unique_id, name
        super().__init__(
            coordinator,
            context="location",
            name_suffix="Location",
        )

    @property
    def latitude(self) -> float | None:
        """Return latitude value of the device."""
        return self.coordinator.data.latitude

    @property
    def longitude(self) -> float | None:
        """Return longitude value of the device."""
        return self.coordinator.data.longitude

    @property
    def source_type(self) -> SourceType:
        """Return the source type, eg gps or router, of the device."""
        return SourceType.GPS

    @property
    def icon(self) -> str:
        """Return the icon of the motorcycle."""
        return "mdi:motorcycle"
