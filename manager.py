# Simulate the memory manager that manages the memory blocks, pools, and arenas.

from block import Block
from pool import Pool
from arena import Arena
from pympler import asizeof

# memorymanager is a singleton class
# only three methods should ever be called/exposed on this class,
# that being get_instance, allocate, and deallocate
# the rest of the methods are private and should not be called

# when allocate is called:
# - Create a block for the object
# - Check if there is a pool that can fit the block
# - If there is no pool that can fit the block, create a new pool
# - Check if there is an arena that can fit the pool
# - If there is no arena that can fit the pool, create a new arena
# - Add the block to the pool

# when deallocate is called:
# - Find the block in the pool
# - Remove the block from the pool
# - If the pool is empty, remove the pool from the arena
# - If the arena is empty, remove the arena from the memory manager

class MemoryManager:
    _instance = None

    def __init__(self):
        if MemoryManager._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.arenas = []
            MemoryManager._instance = self

    @staticmethod
    def get_instance():
        if MemoryManager._instance is None:
            MemoryManager()
        return MemoryManager._instance


    def _allocate_block(self, obj):
        block = Block(obj)
        for arena in self.arenas:
            for pool in arena.pools:
                # check if the pool has enough space for the block
                if pool.check_pool(block.block_size):
                    pool.blocks.append(block)
                    pool.bytes += block.block_size
                    return block
        return None

    def _allocate_pool(self, block_size):
        pool = Pool(block_size)
        for arena in self.arenas:
            # check if the arena has enough space for the pool
            if arena.check_arena(pool.MAXSIZE):
                arena.pools.append(pool)
                arena.bytes += pool.MAXSIZE
                return pool
        # If no existing arena can fit the pool, create a new arena
        arena = self._allocate_arena()
        arena.pools.append(pool)
        arena.bytes += pool.MAXSIZE
        return pool

    def _allocate_arena(self):
        arena = Arena()
        self.arenas.append(arena)
        return arena

    def allocate(self, obj):
        block = self._allocate_block(obj)
        # if there is no block since no pool, create a new pool
        if block is None:
            pool = self._allocate_pool(asizeof.asizeof(obj))
            block = Block(obj)
            pool.blocks.append(block)
            pool.bytes += block.block_size


    def deallocate(self, block):
        for arena in self.arenas:
            for pool in arena.pools:
                if block in pool.blocks:
                    # remove the block from the pool
                    pool.blocks.remove(block)
                    pool.bytes -= block.block_size

                    # if the pool is empty, remove the pool from the arena
                    if len(pool.blocks) == 0:
                        arena.pools.remove(pool)
                        arena.bytes -= pool.MAXSIZE

                    # if the arena is empty, remove the arena from the memory manager
                    if len(arena.pools) == 0:
                        self.arenas.remove(arena)

                    return True
        return False
