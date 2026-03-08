from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)

from custom_components.zero_motorcycles.coordinator import ZeroDataCoordinator

from .entity import ZeroMotorcycleEntity


async def async_setup_entry(hass, entry, async_add_entities) -> None:  # noqa: ANN001, ARG001
    """Set up Zero binary sensors."""
    coordinator = entry.runtime_data.coordinator
    async_add_entities(
        [
            ZeroChargingBinarySensor(coordinator),
            ZeroPluggedInBinarySensor(coordinator),
            ZeroIgnitionBinarySensor(coordinator),
            ZeroTipOverBinarySensor(coordinator),
        ]
    )


class ZeroChargingBinarySensor(ZeroMotorcycleEntity, BinarySensorEntity):
    _attr_device_class = BinarySensorDeviceClass.BATTERY_CHARGING

    def __init__(self, coordinator: ZeroDataCoordinator):
        super().__init__(coordinator, context="is_charging", name="Charging")

    @property
    def is_on(self) -> bool:
        return self.coordinator.data.is_charging


class ZeroIgnitionBinarySensor(ZeroMotorcycleEntity, BinarySensorEntity):
    _attr_device_class = BinarySensorDeviceClass.POWER

    def __init__(self, coordinator: ZeroDataCoordinator):
        super().__init__(coordinator, context="ignition", name="Ignition")

    @property
    def is_on(self) -> bool:
        return self.coordinator.data.ignition


class ZeroTipOverBinarySensor(ZeroMotorcycleEntity, BinarySensorEntity):
    _attr_device_class = BinarySensorDeviceClass.PROBLEM

    def __init__(self, coordinator: ZeroDataCoordinator):
        super().__init__(coordinator, context="tipped_over", name="Tip-over")

    @property
    def is_on(self) -> bool:
        return self.coordinator.data.is_tipped_over


class ZeroPluggedInBinarySensor(ZeroMotorcycleEntity, BinarySensorEntity):
    _attr_device_class = BinarySensorDeviceClass.POWER

    def __init__(self, coordinator: ZeroDataCoordinator):
        super().__init__(coordinator, context="plugged_in", name="Plugged In")

    @property
    def is_on(self) -> bool:
        return self.coordinator.data.is_plugged_in
