#!/usr/bin/env python3
"""tasks 4"""
import asyncio
from typing import List
wait_n = __import__('1-concurrent_coroutines').wait_n


async def task_wait_n(n: int, max_delay: int = 10) -> List[float]:
    """
        Take the code from wait_n and alter it into a
        new function task_wait_n. The code is nearly
        identical to wait_n except task_wait_random
        is being called.
    """
    delays = await asyncio.gather(*(wait_n(max_delay) for _ in range(n)))

    return sorted(delays)
