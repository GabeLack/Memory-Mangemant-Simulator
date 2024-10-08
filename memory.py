"""
NAME
    memory

DESCRIPTION
    This module provides classes for memory management, including Arena, Pool, and Block.
    It uses the MemoryAnalyzer class to analyze and track memory usage of Python objects.

CLASSES
    Arena
        A class to represent an Arena for memory management.

        Methods defined here:
            __init__(self)
                Initializes the Arena with an empty list of pools and zero bytes.

            check_arena(self, pool_size=4000) -> bool
                Checks if adding a new pool would exceed the maximum size of the arena.

    Pool
        A class to represent a Pool for memory management.

        Methods defined here:
            __init__(self, block_size)
                Initializes the Pool with an empty list of blocks, zero bytes, and a specified block size.

            check_pool(self, block_size) -> bool
                Checks if adding a new block would exceed the maximum size of the pool.

    Block
        A class to represent a Block for memory management.

        Methods defined here:
            __init__(self, obj)
                Initializes the Block with an object and measures its size.
"""

import math
from analyzer import MemoryAnalyzer

class Arena:
    """
    A class to represent an Arena for memory management.

    Attributes:
        MAXSIZE (int): The maximum size of the arena.
        pools (list): A list to store pools in the arena.
        bytes (int): The current size of the arena in bytes.

    Methods:
        check_arena(pool_size=4000) -> bool:
            Checks if adding a new pool would exceed the maximum size of the arena.
    """
    MAXSIZE = 256000

    def __init__(self):
        """
        Initializes the Arena with an empty list of pools and zero bytes.
        """
        self.pools = []
        self.bytes = 0

    def check_arena(self, pool_size=4000):
        """
        Checks if adding a new pool would exceed the maximum size of the arena.

        Args:
            pool_size (int): The size of the pool to be added. Default is 4000.

        Returns:
            bool: True if the pool can be added without exceeding the maximum size, False otherwise.

        Raises:
            TypeError: If pool_size is not an integer.
        """
        if not isinstance(pool_size, int):
            raise TypeError("Pool size must be an integer")
        return self.bytes + pool_size <= self.MAXSIZE and pool_size == Pool.MAXSIZE

class Pool:
    """
    A class to represent a Pool for memory management.

    Attributes:
        MAXSIZE (int): The maximum size of the pool.
        blocks (list): A list to store blocks in the pool.
        bytes (int): The current size of the pool in bytes.
        block_size (int): The size of each block in the pool.

    Methods:
        check_pool(block_size) -> bool:
            Checks if adding a new block would exceed the maximum size of the pool.
    """
    MAXSIZE = 4000

    def __init__(self, block_size):
        """
        Initializes the Pool with an empty list of blocks, zero bytes, and a specified block size.

        Args:
            block_size (int): The size of each block in the pool.

        Raises:
            TypeError: If block_size is not an integer.
            ValueError: If block_size is not divisible by 8 or is zero.
        """
        if not isinstance(block_size, int):
            raise TypeError("Block size must be an integer")
        if block_size % 8 != 0 or block_size == 0:
            raise ValueError("Block size must be divisible by 8")

        self.blocks = []
        self.bytes = 0
        self.block_size = block_size

    def check_pool(self, block_size):
        """
        Checks if adding a new block would exceed the maximum size of the pool.

        Args:
            block_size (int): The size of the block to be added.

        Returns:
            bool: True if the block can be added without exceeding the maximum size, False otherwise.

        Raises:
            TypeError: If block_size is not an integer.
        """
        if not isinstance(block_size, int):
            raise TypeError("Block size must be an integer")
        return self.bytes + block_size <= self.MAXSIZE and self.block_size == block_size

class Block:
    """
    A class to represent a Block for memory management.

    Attributes:
        MAXSIZE (int): The maximum size of the block.
        obj (object): The object stored in the block.
        block_size (int): The size of the block.

    Methods:
        __init__(obj):
            Initializes the Block with an object and measures its size.
    """
    MAXSIZE = 512

    def __init__(self, obj):
        """
        Initializes the Block with an object and measures its size.

        Args:
            obj (object): The object to be stored in the block.

        Raises:
            ValueError: If the size of the object exceeds the maximum block size.
        """
        analyzer = MemoryAnalyzer.get_instance()
        size = analyzer.measure_size(obj)
        if size > self.MAXSIZE:
            raise ValueError("Size too large")

        self.obj = obj
        self.block_size = size
