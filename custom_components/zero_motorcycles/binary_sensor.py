from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
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
    def __init__(self, coordinator: ZeroDataCoordinator):
        super().__init__(coordinator, context="is_charging")
        self.entity_description = BinarySensorEntityDescription(
            key="is_charging",
            name="Charging",
            device_class=BinarySensorDeviceClass.BATTERY_CHARGING,
        )

    @property
    def is_on(self) -> bool:
        return self.coordinator.data.is_charging


class ZeroIgnitionBinarySensor(ZeroMotorcycleEntity, BinarySensorEntity):
    def __init__(self, coordinator: ZeroDataCoordinator):
        super().__init__(coordinator, context="ignition")
        self.entity_description = BinarySensorEntityDescription(
            key="ignition",
            name="Ignition",
            device_class=BinarySensorDeviceClass.POWER,
        )

    @property
    def is_on(self) -> bool:
        return self.coordinator.data.ignition


class ZeroTipOverBinarySensor(ZeroMotorcycleEntity, BinarySensorEntity):
    def __init__(self, coordinator: ZeroDataCoordinator):
        super().__init__(coordinator, context="tipped_over")
        self.entity_description = BinarySensorEntityDescription(
            key="tipped_over",
            name="Tipped Over",
            device_class=BinarySensorDeviceClass.PROBLEM,
        )

    @property
    def is_on(self) -> bool:
        return self.coordinator.data.is_tipped_over


class ZeroPluggedInBinarySensor(ZeroMotorcycleEntity, BinarySensorEntity):
    _attr_device_class = BinarySensorDeviceClass.POWER

    def __init__(self, coordinator: ZeroDataCoordinator):
        super().__init__(coordinator, context="plugged_in")
        self.entity_description = BinarySensorEntityDescription(
            key="plugged_in",
            name="Plugged In",
            device_class=BinarySensorDeviceClass.POWER,
        )

    @property
    def is_on(self) -> bool:
        return self.coordinator.data.is_plugged_in
