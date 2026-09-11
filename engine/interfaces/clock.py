# engine/interfaces/clock.py
"""
Clock abstraction Protocol for testability and deterministic simulation.
Conforms to Constraint C1 (pure Python, zero framework dependencies).
"""
from datetime import datetime, timezone
from typing import Protocol, runtime_checkable


@runtime_checkable
class ClockPort(Protocol):
    """Protocol for providing current UTC time."""

    def now(self) -> datetime:
        """Returns the current UTC timestamp."""
        ...


class SystemClock:
    """Default implementation using the system wall clock in UTC."""

    def now(self) -> datetime:
        return datetime.now(timezone.utc)


__all__ = ["ClockPort", "SystemClock"]
