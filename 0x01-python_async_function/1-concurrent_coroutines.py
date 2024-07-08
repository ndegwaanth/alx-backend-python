#!/usr/bin/env python3
"""Multiple coroutines"""

import asyncio
from typing import List
wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int = 10) -> List[float]:
    """
        spawn wait_random n times with
        the specified max_delay
    """
    delays = await asyncio.gather(*(wait_random(max_delay) for _ in range(n)))

    return sorted(delays)
