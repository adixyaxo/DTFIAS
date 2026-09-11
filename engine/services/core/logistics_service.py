# engine/services/core/logistics_service.py
"""
Domain Logistics Service for fuel burn-rate modeling and supply chain management.
Conforms to Constraint C1 (pure Python, zero HTTP/DB framework imports).
"""
from datetime import datetime, timedelta
from typing import Any, Optional

from engine.interfaces.clock import ClockPort, SystemClock


class LogisticsService:
    """Core domain logic for Antarctic station logistics and fuel modeling."""

    def __init__(self, clock: Optional[ClockPort] = None) -> None:
        self.clock = clock or SystemClock()

    def predict_fuel_burn_rate(
        self,
        current_farm_capacity_kl: float,
        daily_consumption_kl: float,
        is_winter: bool
    ) -> dict[str, Any]:
        """
        Fuel Burn-Rate Modeling:
        Project remaining operational days based on current farm capacity and daily consumption.
        Predicts next resupply window from main farm to the day tank.
        
        Rules:
        - Winter consumption is inherently higher. If 'is_winter' is true, pad daily_consumption_kl by 15%.
        - Main farm is 296 kL total. Day tank is 13.6 kL.
        - Transfer to day tank should occur when day tank drops to 30% (approx every 8-10 days normally).
        """
        effective_daily_consumption = daily_consumption_kl * 1.15 if is_winter else daily_consumption_kl
        
        if effective_daily_consumption <= 0:
            return {
                "remaining_days": 999,
                "status": "NORMAL",
                "next_transfer_days": 999
            }

        remaining_days = current_farm_capacity_kl / effective_daily_consumption
        
        # Day tank math (assuming day tank is filled to 13.6 kL)
        # We need to transfer when day tank reaches 30% capacity (4.08 kL used, 9.52 kL remaining? 
        # Actually 30% of 13.6 is 4.08 kL remaining. So 9.52 kL consumed.)
        usable_day_tank_kl = 13.6 * 0.70 
        next_transfer_days = usable_day_tank_kl / effective_daily_consumption

        status = "NORMAL"
        priority = "NONE"
        alerts = []

        if remaining_days < 60:
            status = "CRITICAL"
            priority = "HIGH"
            alerts.append(f"CRITICAL: Bulk fuel reserves below 60 days ({round(remaining_days, 1)} days left). Immediate resupply scheduling required.")
        elif remaining_days < 120:
            status = "WARNING"
            priority = "MEDIUM"
            alerts.append(f"Bulk fuel reserves below 120 days ({round(remaining_days, 1)} days left).")

        return {
            "current_farm_capacity_kl": current_farm_capacity_kl,
            "effective_daily_consumption_kl": round(effective_daily_consumption, 2),
            "remaining_operational_days": int(remaining_days),
            "days_until_next_day_tank_transfer": round(next_transfer_days, 1),
            "status": status,
            "priority": priority,
            "alerts": alerts
        }

__all__ = ["LogisticsService"]
