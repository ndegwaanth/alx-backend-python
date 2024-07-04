#!/usr/bin/env python3
"""Basic annotations - to_kv"""

from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """
        type-annotated function to_kv that takes string
        and int as arguments and returns a list
    """

    return [k, v**2]
