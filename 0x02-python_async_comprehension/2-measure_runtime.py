#!/usr/bin/env python3
"""2. Run time for four parallel comprehensions"""
import asyncio
import time
async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """
    Import async_comprehension from the previous file and
    write a measure_runtime coroutine that will execute
    async_comprehension four times in parallel using asyncio.gather
    """
    start = time.perf_counter()
    await asyncio.gather(
            async_comprehension(), async_comprehension(),
            async_comprehension(), async_comprehension())
    end = time.perf_counter()

    return end - start
