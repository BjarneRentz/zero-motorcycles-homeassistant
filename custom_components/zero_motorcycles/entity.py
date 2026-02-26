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

    @property
    def available(self):
        return self.coordinator.last_update_success

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.data.vin)},
            name=f"{self.coordinator.data.model_year} {self.coordinator.data.model_name}",
            manufacturer="Zero Motorcycles",
            model=self.coordinator.data.model_name,
            sw_version=self.coordinator.data.software_version,
            hw_version=f"Unit {self.coordinator.data.unit_number}",
        )
