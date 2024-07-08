#!/usr/bin/env python

import asyncio
from typing import List
from .0-basic_async_syntax import wait_random


async def wait_n(n: int, max_delay: int = 10) -> List[float]:
    delays = await asyncio.gather(*(wait_random(max_delay) for _ in range(n)))

    return sorted(delays)
