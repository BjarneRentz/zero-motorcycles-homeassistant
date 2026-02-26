"""Custom types."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import ZeroApiClient
    from .coordinator import ZeroDataCoordinator


type ZeroConfigEntry = ConfigEntry[ZeroData]


@dataclass
class ZeroData:
    """Data for the Blueprint integration."""

    client: ZeroApiClient
    coordinator: ZeroDataCoordinator
    integration: Integration
