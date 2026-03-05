"""Sensor entities for Zero Motorcycles integration."""

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import UnitOfLength, UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.zero_motorcycles.coordinator import ZeroDataCoordinator
from custom_components.zero_motorcycles.data import ZeroConfigEntry, ZeroData

from .entity import ZeroMotorcycleEntity


async def async_setup_entry(
    _: HomeAssistant,
    entry: ZeroConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Zero location tracker from a config entry."""
    # Assuming your entry.runtime_data holds the coordinator directly
    # or via a data object. Adjust according to your __init__.py logic.
    data_container: ZeroData = entry.runtime_data

    async_add_entities(
        [
            ZeroBatterySensor(data_container.coordinator),
            ZeroOdometerSensor(data_container.coordinator),
            ZeroChargingTimeLeftSensor(data_container.coordinator),
        ]
    )


class ZeroBatterySensor(ZeroMotorcycleEntity, SensorEntity):
    """Battery State of Charge Sensor."""

    def __init__(self, coordinator: ZeroDataCoordinator) -> None:
        """Initialize the battery sensor."""
        # We pass 'soc' as the context for the unique_id
        super().__init__(coordinator, context="soc", name_suffix="State of Charge")
        self._attr_name = "SoC"
        self._attr_device_class = SensorDeviceClass.BATTERY
        self._attr_native_unit_of_measurement = "%"

    @property
    def native_value(self) -> int:
        """Return the state of charge percentage."""
        return self.coordinator.data.soc


class ZeroOdometerSensor(ZeroMotorcycleEntity, SensorEntity):
    """Mileage/Odometer sensor."""

    _attr_device_class = SensorDeviceClass.DISTANCE
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_native_unit_of_measurement = UnitOfLength.KILOMETERS

    def __init__(self, coordinator: ZeroDataCoordinator) -> None:
        """Initialize the odometer sensor."""
        super().__init__(coordinator, context="mileage", name_suffix="Odometer")

    @property
    def native_value(self) -> float:
        """Return the mileage in kilometers."""
        return self.coordinator.data.mileage


class ZeroChargingTimeLeftSensor(ZeroMotorcycleEntity, SensorEntity):
    """Time remaining until charge complete."""

    _attr_device_class = SensorDeviceClass.DURATION
    _attr_native_unit_of_measurement = UnitOfTime.MINUTES

    def __init__(self, coordinator: ZeroDataCoordinator) -> None:
        """Initialize the charging time left sensor."""
        super().__init__(
            coordinator,
            context="remaining_charging_time",
            name_suffix="Remaining Charging Time",
        )

    @property
    def native_value(self) -> int | None:
        """Return the time remaining until charge complete in minutes."""
        return self.coordinator.data.time_to_full_minutes
