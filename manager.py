"""
NAME
    manager

DESCRIPTION
    This module simulates a memory manager that manages memory blocks, pools, and arenas.
    The MemoryManager class is a singleton and provides methods to allocate and deallocate memory.

CLASSES
    MemoryManager
        A singleton class to manage memory blocks, pools, and arenas.

        Methods defined here:
            __init__(self)
                Initializes the MemoryManager with empty lists for arenas, free blocks, free pools, and free arenas.

            get_instance() -> MemoryManager
                Returns the singleton instance of the MemoryManager.

            _allocate_arena(self) -> Arena
                Allocates a new arena or reuses a free arena.

            _allocate_pool(self, block_size) -> Pool
                Allocates a new pool or reuses a free pool.

            _allocate_block(self, obj) -> Block
                Allocates a new block or reuses a free block.

            allocate(self, obj)
                Allocates memory for the given object.

            deallocate(self, block) -> bool
                Deallocates the given block(/pool/arena) and sets it for reuse.
"""

from memory import Arena, Pool, Block
from pympler import asizeof

class MemoryManager:
    """
    A singleton class to manage memory blocks, pools, and arenas.

    Attributes:
        _instance (MemoryManager): The singleton instance of the MemoryManager.
        arenas (list): A list to store arenas.
        free_blocks (list): A list to store free blocks.
        free_pools (list): A list to store free pools.
        free_arenas (list): A list to store free arenas.

    Methods:
        get_instance() -> MemoryManager:
            Returns the singleton instance of the MemoryManager.
        _allocate_arena() -> Arena:
            Allocates a new arena or reuses a free arena.
        _allocate_pool(block_size) -> Pool:
            Allocates a new pool or reuses a free pool.
        _allocate_block(obj) -> Block:
            Allocates a new block or reuses a free block.
        allocate(obj):
            Allocates memory for the given object.
        deallocate(block) -> bool:
            Deallocates the given block(/pool/arena) and sets it for reuse.
    """
    _instance = None

    def __init__(self):
        """
        Initializes the MemoryManager with empty lists for arenas, free blocks, free pools, and free arenas.

        Raises:
            Exception: If an instance of MemoryManager already exists.
        """
        if MemoryManager._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.arenas = []
            self.free_blocks = []
            self.free_pools = []
            self.free_arenas = []
            MemoryManager._instance = self

    @staticmethod
    def get_instance():
        """
        Returns the singleton instance of the MemoryManager.

        Returns:
            MemoryManager: The singleton instance of the MemoryManager.
        """
        if MemoryManager._instance is None:
            MemoryManager()
        return MemoryManager._instance

    def _allocate_arena(self):
        """
        Allocates a new arena or reuses a free arena.

        Returns:
            Arena: The allocated or reused arena.
        """
        if self.free_arenas:
            # Check if there is a free arena
            arena = self.free_arenas.pop()
        else:
            # If there is no free arena, create a new arena
            arena = Arena()

        self.arenas.append(arena)
        return arena

    def _allocate_pool(self, block_size):
        """
        Allocates a new pool or reuses a free pool.

        Args:
            block_size (int): The size of the block to be added to the pool.

        Returns:
            Pool: The allocated or reused pool.
        """
        if self.free_pools:
            # Check if there is a free pool
            pool = self.free_pools.pop()
            pool.block_size = block_size
        else:
            # If there is no free pool, create a new pool
            pool = Pool(block_size)

        for arena in self.arenas:
            # Check if the arena has enough space for the pool
            if arena.check_arena(pool.MAXSIZE):
                arena.pools.append(pool)
                arena.bytes += pool.MAXSIZE
                return pool

        # If no existing arena can fit the pool, create a new arena
        arena = self._allocate_arena()
        arena.pools.append(pool)
        arena.bytes += pool.MAXSIZE
        return pool

    def _allocate_block(self, obj):
        """
        Allocates a new block or reuses a free block.

        Args:
            obj (object): The object to be stored in the block.

        Returns:
            Block: The allocated or reused block.

        Raises:
            ValueError: If the size of the object exceeds the maximum block size.
        """
        if self.free_blocks:
            # Check if there is a free block
            block = self.free_blocks.pop()

            size = asizeof.asizeof(obj)
            if size > block.MAXSIZE:
                raise ValueError("Size too large")
            block.obj = obj
            block.block_size = size
        else:
            # If there is no free block, create a new block
            block = Block(obj)

        for arena in self.arenas:
            if arena.check_arena(4000):
                for pool in arena.pools:
                    # Check if the pool has enough space for the block
                    if pool.check_pool(block.block_size):
                        pool.blocks.append(block)
                        pool.bytes += block.block_size
                        return block
        return None

    def allocate(self, obj):
        """
        Allocates memory for the given object.

        Args:
            obj (object): The object to be allocated memory.

        Raises:
            ValueError: If the size of the object exceeds the maximum block size.
        """
        block = self._allocate_block(obj)
        # If there is no block since no pool, create a new pool
        if block is None:
            block = Block(obj)
            pool = self._allocate_pool(block.block_size)
            pool.blocks.append(block)
            pool.bytes += block.block_size

    def deallocate(self, block):
        """
        Deallocates the given block and reuses it if possible.

        Args:
            block (Block): The block to be deallocated.

        Returns:
            bool: True if the block was successfully deallocated, False otherwise.
        """
        for arena in self.arenas:
            for pool in arena.pools:
                if block in pool.blocks:
                    # Remove the block from the pool
                    pool.blocks.remove(block)
                    pool.bytes -= block.block_size

                    # Save the block for reuse
                    self.free_blocks.append(block)

                    # If the pool is empty, remove the pool from the arena
                    if pool.bytes == 0:
                        arena.pools.remove(pool)
                        arena.bytes -= pool.MAXSIZE

                        # Save the pool for reuse
                        self.free_pools.append(pool)

                    # If the arena is empty, remove the arena from the memory manager
                    if arena.bytes == 0:
                        self.arenas.remove(arena)

                        # Save the arena for reuse
                        self.free_arenas.append(arena)

                    return True
        return False
