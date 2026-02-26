"""Sensor platform for Zero Motorcycles."""

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN
from .entity import ZeroMotorcycleEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    """Set up Zero Motorcycle sensor entities from a config entry."""
    coordinator = entry.runtime_data.coordinator
    # For now, create a single entity with a static unique_id and name
    unique_id = f"{DOMAIN}_motorcycle_1"
    name = "Zero Motorcycle"
    async_add_entities([ZeroMotorcycleEntity(coordinator, unique_id, name)])
