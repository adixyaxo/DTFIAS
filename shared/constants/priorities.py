# shared/constants/priorities.py
"""
Write Buffer & Synchronization Priority Levels.
P0 alerts broadcast before P1 telemetry.
"""
from enum import IntEnum


class Priority(IntEnum):
    P0_CRITICAL_ALERT = 0
    P1_COMMAND = 1
    P2_TELEMETRY = 2
    P3_OBSERVATION = 3


# Queue priority ordering
PRIORITY_ORDER = [
    Priority.P0_CRITICAL_ALERT,
    Priority.P1_COMMAND,
    Priority.P2_TELEMETRY,
    Priority.P3_OBSERVATION,
]
