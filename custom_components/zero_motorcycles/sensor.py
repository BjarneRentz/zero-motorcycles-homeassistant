from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import UnitOfLength, UnitOfTime

from custom_components.zero_motorcycles.data import ZeroData

from .entity import ZeroMotorcycleEntity


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the Zero location tracker from a config entry."""
    # Assuming your entry.runtime_data holds the coordinator directly
    # or via a data object. Adjust according to your __init__.py logic.
    dataContainer: ZeroData = entry.runtime_data
    async_add_entities(
        [
            ZeroBatterySensor(dataContainer.coordinator),
            ZeroOdometerSensor(dataContainer.coordinator),
            ZeroChargingTimeLeftSensor(dataContainer.coordinator),
        ]
    )


class ZeroBatterySensor(ZeroMotorcycleEntity, SensorEntity):
    """Battery State of Charge Sensor."""

    def __init__(self, coordinator):
        # We pass 'soc' as the context for the unique_id
        super().__init__(coordinator, context="soc", name_suffix="State of Charge")
        self._attr_name = "SoC"
        self._attr_device_class = SensorDeviceClass.BATTERY
        self._attr_native_unit_of_measurement = "%"

    @property
    def native_value(self) -> int:
        return self.coordinator.data.soc


class ZeroOdometerSensor(ZeroMotorcycleEntity, SensorEntity):
    """Mileage/Odometer sensor."""

    _attr_device_class = SensorDeviceClass.DISTANCE
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_native_unit_of_measurement = UnitOfLength.KILOMETERS

    def __init__(self, coordinator):
        super().__init__(coordinator, context="mileage", name_suffix="Odometer")

    @property
    def native_value(self) -> float:
        return self.coordinator.data.mileage


class ZeroChargingTimeLeftSensor(ZeroMotorcycleEntity, SensorEntity):
    """Time remaining until charge complete."""

    _attr_device_class = SensorDeviceClass.DURATION
    _attr_native_unit_of_measurement = UnitOfTime.MINUTES

    def __init__(self, coordinator):
        super().__init__(
            coordinator,
            context="remaining_charging_time",
            name_suffix="Remaining Charging Time",
        )

    @property
    def native_value(self) -> int | None:
        return self.coordinator.data.time_to_full_minutes
