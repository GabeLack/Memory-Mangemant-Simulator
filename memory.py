import math
from analyzer import MemoryAnalyzer

class Arena:
    MAXSIZE = 256000

    def __init__(self):
        self.pools = []
        self.bytes = 0
        self.free = True

    def check_arena(self, pool_size):
        # Check if adding the new pool would exceed the maximum size
        return self.bytes + pool_size <= self.MAXSIZE and pool_size == Pool.MAXSIZE

class Pool:
    MAXSIZE = 4000

    def __init__(self, block_size):
        if not isinstance(block_size, int):
            raise TypeError("Block size must be an integer")
        if block_size % 8 != 0:
            raise ValueError("Block size must be divisible by 8")

        self.blocks = []
        self.bytes = 0
        self.block_size = block_size
        self.free = True

    def check_pool(self, block_size):
        return self.bytes + block_size <= self.MAXSIZE and self.block_size == block_size

class Block:
    MAXSIZE = 512

    def __init__(self, obj):
        # Measure the size of the object in a multiple of 8 bytes
        size = MemoryAnalyzer.measure_size(obj)
        if size > self.MAXSIZE:
            raise ValueError("Size too large")

        self.obj = obj
        self.block_size = size
        self.free = True
