from custom_components.zero_motorcycles.models import ZeroBikeData

# Year Mapping (10th Character)
YEAR_MAP = {
    "K": 2019,
    "L": 2020,
    "M": 2021,
    "N": 2022,
    "P": 2023,
    "R": 2024,
    "S": 2025,
    "T": 2026,
}
MODELS = {
    "FA": "SR/F",
    "FB": "SR/S",
    "FC": "SR",
    "FD": "DSR/X",
    "FE": "SR/F (Premium)",
}


class ZeroParser:
    """Decodes raw Mongol API responses into ZeroBikeData objects."""

    @staticmethod
    def parse_telemetry(raw_json: list) -> ZeroBikeData:
        """Parses the first item in the Mongol API list response."""
        if not raw_json or not isinstance(raw_json, list):
            raise ValueError("Invalid API response format")

        data = raw_json[0]
        vin = data.get("name", "Unknown")

        # Decode VIN for model/year (using the logic from our previous step)
        # Assuming you've integrated the decode_zero_vin function here
        decoded = ZeroParser.decode_zero_vin(vin)

        return ZeroBikeData(
            unit_number=data.get("unitnumber"),
            vin=vin,
            model_name=decoded["model"],
            model_year=decoded["year"],
            # Convering strings to proper types
            soc=int(data.get("soc", 0)),
            mileage=float(data.get("mileage", 0)),
            is_charging=data.get("charging") == 1,
            is_plugged_in=data.get("pluggedin") == 1,
            is_connected=True,
            latitude=float(data.get("latitude")) if data.get("latitude") else None,
            longitude=float(data.get("longitude")) if data.get("longitude") else None,
            software_version=data.get("software_version", "Unknown"),
            ignition=data.get("ignition") == "1",
            is_tipped_over=data.get("tippedover") == 1,
            time_to_full_minutes=int(data.get("chargingtimeleft", 0))
            if data.get("pluggedin") == 1
            else None,
            is_charge_complete=data.get("chargecomplete") == 1,
        )

    @staticmethod
    def decode_zero_vin(vin: str):
        """Decodes a Zero Motorcycle VIN into model and year info."""
        if not vin or len(vin) < 17:
            return {"model": "Unknown", "year": "Unknown"}

        # Model/Platform Mapping (Positions 5 and 6 are key for Gen 3)
        # This is based on common community data for Model 6/Gen 3 bikes
        platform_code = vin[4:6]  # e.g., 'FA' or 'FB'

        model_name = MODELS.get(platform_code, f"Zero Gen3 ({platform_code})")
        model_year = YEAR_MAP.get(vin[9], f"20{vin[9]}")  # Fallback for numeric years

        return {
            "model": model_name,
            "year": model_year,
        }
