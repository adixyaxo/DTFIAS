# infrastructure/resilience/in_process_write_buffer.py
"""
In-Memory implementation of WriteBufferPort.
Provides store-and-forward resilience for polar SATCOM outages.
"""
import asyncio
from typing import Any
import uuid

from engine.interfaces.write_buffer import WriteBufferPort
from shared.constants.priorities import Priority


class InProcessWriteBuffer(WriteBufferPort):
    """
    Asyncio PriorityQueue-backed write buffer.
    Items are tuples of (priority, sequence_number, item).
    """

    def __init__(self) -> None:
        self._queue: asyncio.PriorityQueue = asyncio.PriorityQueue()
        self._seq = 0
        self._lock = asyncio.Lock()

    async def enqueue(self, item: Any, priority: Priority = Priority.P2_TELEMETRY) -> str:
        async with self._lock:
            self._seq += 1
            seq = self._seq
        # Priority Queue sorts by lowest value first.
        # Priority enum assigns 0 to P0 (highest), 1 to P1, etc.
        # seq ensures FIFO ordering for items of the same priority.
        await self._queue.put((priority.value, seq, item))
        return str(uuid.uuid4())

    async def dequeue(self) -> Any | None:
        if self._queue.empty():
            return None
        priority, seq, item = await self._queue.get()
        return item

    async def peek(self) -> Any | None:
        # PriorityQueue in python does not have an official peek method without removing.
        # But for an in-memory queue, we can just check the internal list.
        if self._queue.empty():
            return None
        # _queue is the internal heapq used by asyncio.PriorityQueue
        return self._queue._queue[0][2]

    async def size(self) -> int:
        return self._queue.qsize()

    async def clear(self) -> None:
        while not self._queue.empty():
            try:
                self._queue.get_nowait()
            except asyncio.QueueEmpty:
                break


__all__ = ["InProcessWriteBuffer"]
