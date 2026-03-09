"""Sensor entities for Zero Motorcycles integration."""

from datetime import datetime
import stat
from unicodedata import category

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import PERCENTAGE, EntityCategory, UnitOfLength, UnitOfTime
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
            ZeroLastReportedUpdateSensor(data_container.coordinator),
        ]
    )


class ZeroBatterySensor(ZeroMotorcycleEntity, SensorEntity):
    """Battery State of Charge Sensor."""

    def __init__(self, coordinator: ZeroDataCoordinator) -> None:
        """Initialize the battery sensor."""
        # We pass 'soc' as the context for the unique_id
        super().__init__(coordinator, context="soc")

        self.entity_description = SensorEntityDescription(
            key="soc",
            name="State of Charge",
            device_class=SensorDeviceClass.BATTERY,
            native_unit_of_measurement=PERCENTAGE,
            state_class=SensorStateClass.MEASUREMENT,
        )

    @property
    def native_value(self) -> int:
        """Return the state of charge percentage."""
        return self.coordinator.data.soc


class ZeroOdometerSensor(ZeroMotorcycleEntity, SensorEntity):
    """Mileage/Odometer sensor."""

    def __init__(self, coordinator: ZeroDataCoordinator) -> None:
        """Initialize the odometer sensor."""
        super().__init__(coordinator, context="mileage")

        self.entity_description = SensorEntityDescription(
            key="mileage",
            name="Mileage",
            device_class=SensorDeviceClass.DISTANCE,
            native_unit_of_measurement=UnitOfLength.KILOMETERS,
            state_class=SensorStateClass.TOTAL_INCREASING,
        )

    @property
    def native_value(self) -> float:
        """Return the mileage in kilometers."""
        return self.coordinator.data.mileage


class ZeroChargingTimeLeftSensor(ZeroMotorcycleEntity, SensorEntity):
    """Time remaining until charge complete."""

    def __init__(self, coordinator: ZeroDataCoordinator) -> None:
        """Initialize the charging time left sensor."""
        super().__init__(coordinator, context="remaining_charging_time")

        self.entity_description = SensorEntityDescription(
            key="remaining_charging_time",
            name="Remaining Charging Time",
            device_class=SensorDeviceClass.DURATION,
            native_unit_of_measurement=UnitOfTime.MINUTES,
            state_class=SensorStateClass.MEASUREMENT,
        )

    @property
    def native_value(self) -> int | None:
        """Return the time remaining until charge complete in minutes."""
        return self.coordinator.data.time_to_full_minutes


class ZeroLastReportedUpdateSensor(ZeroMotorcycleEntity, SensorEntity):
    """Last reported update time from the motorcycle."""

    def __init__(self, coordinator: ZeroDataCoordinator) -> None:
        """Initialize the last update sensor."""
        super().__init__(coordinator, context="last_update")

        self.entity_description = SensorEntityDescription(
            key="last_update",
            name="Last Reported Update",
            device_class=SensorDeviceClass.TIMESTAMP,
            entity_category=EntityCategory.DIAGNOSTIC,
        )

    @property
    def native_value(self) -> datetime | None:
        """Return the last update time as an ISO 8601 string."""
        if self.coordinator.data.last_updated:
            return self.coordinator.data.last_updated
        return None
