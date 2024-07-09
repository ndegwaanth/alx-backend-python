#!/usr/bin/env python3
"""1.Async Comprehensions"""
import random
import asyncio
from typing import List
async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    num = [i async for i in async_generator()]

    return num
