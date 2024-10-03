# simulate a block of memory

import math
from pympler import asizeof

class Block:
    MAXSIZE = 512

    def __init__(self, obj):
        size = asizeof.asizeof(obj)
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
