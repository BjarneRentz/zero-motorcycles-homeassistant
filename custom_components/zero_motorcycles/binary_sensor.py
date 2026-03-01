from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)

from .entity import ZeroMotorcycleEntity


async def async_setup_entry(hass, entry, async_add_entities):
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

    def __init__(self, coordinator):
        super().__init__(coordinator, context="is_charging", name_suffix="Charging")

    @property
    def is_on(self) -> bool:
        return self.coordinator.data.is_charging


class ZeroIgnitionBinarySensor(ZeroMotorcycleEntity, BinarySensorEntity):
    _attr_device_class = BinarySensorDeviceClass.POWER

    def __init__(self, coordinator):
        super().__init__(coordinator, context="ignition", name_suffix="Ignition")

    @property
    def is_on(self) -> bool:
        return self.coordinator.data.ignition


class ZeroTipOverBinarySensor(ZeroMotorcycleEntity, BinarySensorEntity):
    _attr_device_class = BinarySensorDeviceClass.PROBLEM

    def __init__(self, coordinator):
        super().__init__(coordinator, context="tipped_over", name_suffix="Tip-over")

    @property
    def is_on(self) -> bool:
        return self.coordinator.data.is_tipped_over


class ZeroPluggedInBinarySensor(ZeroMotorcycleEntity, BinarySensorEntity):
    _attr_device_class = BinarySensorDeviceClass.POWER

    def __init__(self, coordinator):
        super().__init__(coordinator, context="plugged_in", name_suffix="Plugged In")

    @property
    def is_on(self) -> bool:
        return self.coordinator.data.is_plugged_in
