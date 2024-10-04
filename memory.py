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
        return self.bytes + pool_size <= self.MAXSIZE

class Pool:
    MAXSIZE = 4000

    def __init__(self, block_size):
        self.blocks = []
        self.bytes = 0
        self.block_size = block_size
        self.free = True

    def check_pool(self, block_size):
        return self.bytes + block_size <= self.MAXSIZE and self.block_size == block_size

class Block:
    MAXSIZE = 512

    def __init__(self, obj):
        size = MemoryAnalyzer.measure_size(obj)
        allocated_block, size_class_idx = self.bytes_size(size)

        self.obj = obj
        self.block_size = allocated_block
        self.size_class_idx = size_class_idx
        self.free = True

    def bytes_size(self, size):
        size_class_idx = size // 8
        allocated_block = math.ceil(size / 8) * 8

        # check if the size is too large for a block
        if allocated_block > self.MAXSIZE:
            raise ValueError("Size too large")

        return allocated_block, size_class_idx