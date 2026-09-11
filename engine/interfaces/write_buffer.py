# engine/interfaces/write_buffer.py
"""
Write Buffer Protocol for Polar SATCOM store-and-forward resilience.
Conforms to Constraint C1 (pure Python, zero framework dependencies).
"""
from typing import Protocol, TypeVar, Any, runtime_checkable
from shared.constants.priorities import Priority

T = TypeVar("T")


@runtime_checkable
class WriteBufferPort(Protocol):
    """Protocol for prioritized, offline-tolerant store-and-forward write buffers."""

    async def enqueue(self, item: Any, priority: Priority = Priority.P2_TELEMETRY) -> str:
        """Enqueues an item with a specific priority. Returns queued message ID."""
        ...

    async def dequeue(self) -> Any | None:
        """Pops and returns the highest priority item from the buffer."""
        ...

    async def peek(self) -> Any | None:
        """Inspects the next item to be dequeued without removing it."""
        ...

    async def size(self) -> int:
        """Returns the total number of items currently buffered."""
        ...

    async def clear(self) -> None:
        """Clears all buffered entries."""
        ...


__all__ = ["WriteBufferPort"]
