"""Entity for Zero Motorcycle."""

from homeassistant.helpers.entity import DeviceInfo, Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.zero_motorcycles.coordinator import ZeroDataCoordinator

from .const import DOMAIN


class ZeroMotorcycleEntity(CoordinatorEntity[ZeroDataCoordinator], Entity):
    """Representation of a Zero Motorcycle."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: ZeroDataCoordinator, context: str):
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.data.unit_number}_{context}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.data.vin)},
            name=f"{coordinator.data.model_year} {coordinator.data.model_name}",
            manufacturer="Zero Motorcycles",
            model=coordinator.data.model_name,
            sw_version=coordinator.data.software_version,
            hw_version=f"Unit {coordinator.data.unit_number}",
        )

    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success
