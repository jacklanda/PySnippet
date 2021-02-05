#!/bin/python3
# -*- coding: utf-8 -*-

# use lru_cache to accelerate
# your recursive calculation

import sys
import time
from functools import lru_cache

sys.setrecursionlimit(9999)


@lru_cache(maxsize=1024)
def feb(i: int):
    if(i == 0):
        return i
    if(i == 1):
        return 2
    return feb(i-2) + feb(i-1)


while(1):
    start = time.perf_counter()
    num = input("Please input a number to calculate: ")
    print(feb(int(num)))
    end = time.perf_counter()
    print(f"continued time: {end - start}s", end="\n")
