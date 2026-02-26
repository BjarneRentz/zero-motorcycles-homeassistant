""" "Simple data model for Zero Motorcycle telemetry."""

from dataclasses import dataclass


@dataclass
class ZeroBikeData:
    """Refined representation of Zero Motorcycle telemetry."""

    unit_number: str
    vin: str
    model_name: str
    model_year: str
    mileage: float
    soc: int
    is_charging: bool
    is_plugged_in: bool
    is_connected: bool
    is_charge_complete: bool
    time_to_full_minutes: int | None
    latitude: float | None
    longitude: float | None
    software_version: str
    ignition: bool
    is_tipped_over: bool
