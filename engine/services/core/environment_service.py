# engine/services/core/environment_service.py
"""
Domain Environment Service for HVAC optimization and scientific weather analysis.
Conforms to Constraint C1 (pure Python, zero HTTP/DB framework imports).
"""
from datetime import datetime
from uuid import UUID
from typing import Any, Optional

from engine.interfaces.clock import ClockPort, SystemClock


class EnvironmentService:
    """Core domain logic for HVAC control and environmental modeling."""

    def __init__(self, clock: Optional[ClockPort] = None) -> None:
        self.clock = clock or SystemClock()

    def optimize_hvac(
        self,
        indoor_co2_ppm: float,
        indoor_temp_c: float,
        outdoor_temp_c: float,
        current_fresh_air_pct: float
    ) -> dict[str, Any]:
        """
        HVAC Optimization logic:
        Correlate indoor CO2 with fresh air intake and heating demand to optimize fuel.
        Bringing in -40C fresh air costs massive energy to heat. We should only bring in
        fresh air when CO2 levels dictate it to preserve Jet A-1 fuel.
        
        Rules:
        - Optimal CO2 is < 800 ppm. Max allowable is 1000 ppm.
        - If CO2 < 600 ppm, we can safely reduce fresh air intake to save heat.
        - If CO2 > 1000 ppm, we MUST increase fresh air intake despite heating cost.
        """
        recommended_fresh_air_pct = current_fresh_air_pct
        action = "MAINTAIN"
        reason = "CO2 levels within optimal range."

        if indoor_co2_ppm > 1000.0:
            recommended_fresh_air_pct = min(100.0, current_fresh_air_pct + 20.0)
            action = "INCREASE_INTAKE"
            reason = f"CO2 levels critically high ({indoor_co2_ppm} ppm). Increasing fresh air intake for personnel safety."
        elif indoor_co2_ppm < 600.0 and current_fresh_air_pct > 10.0:
            # We can save energy
            recommended_fresh_air_pct = max(10.0, current_fresh_air_pct - 15.0)
            action = "DECREASE_INTAKE"
            reason = f"CO2 levels excellent ({indoor_co2_ppm} ppm). Reducing fresh air intake to conserve thermal energy against {outdoor_temp_c}°C outdoor temp."

        energy_saving_mode = (action == "DECREASE_INTAKE")

        return {
            "indoor_co2_ppm": indoor_co2_ppm,
            "current_fresh_air_pct": current_fresh_air_pct,
            "recommended_fresh_air_pct": round(recommended_fresh_air_pct, 1),
            "action": action,
            "reason": reason,
            "energy_saving_mode_active": energy_saving_mode
        }

__all__ = ["EnvironmentService"]
