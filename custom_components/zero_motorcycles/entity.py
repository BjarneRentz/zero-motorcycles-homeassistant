"""Entity for Zero Motorcycle."""

from homeassistant.helpers.entity import Entity, DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN


class ZeroMotorcycleEntity(CoordinatorEntity, Entity):
    """Representation of a Zero Motorcycle."""

    def __init__(self, coordinator, unique_id, name):
        super().__init__(coordinator)
        self._attr_unique_id = unique_id
        self._attr_name = name
        self._device_info = DeviceInfo(
            identifiers={(DOMAIN, unique_id)},
            name=name,
            manufacturer="Zero Motorcycles",
            model="Unknown",  # Update when model info is available
        )

    @property
    def available(self):
        return self.coordinator.last_update_success

    @property
    def device_info(self) -> DeviceInfo:
        return self._device_info
