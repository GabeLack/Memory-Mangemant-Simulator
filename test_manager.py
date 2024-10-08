"""
NAME
    test_manager

DESCRIPTION
    This module contains unit tests for the MemoryManager class.
    It uses the unittest framework and parameterized tests for various types.

CLASSES
    TestMemoryManager
        Unit tests for the MemoryManager class.

        Methods defined here:
            setUp(self)
                Sets up the test case environment.

            test_get_instance(self)
                Tests the singleton instance of the MemoryManager.

            test_allocate_arena(self)
                Tests the allocation of arenas.

            test_allocate_pool_after_arena(self)
                Tests the allocation of pools after an arena is allocated.

            test_allocate_pool(self)
                Tests the allocation of pools.

            test_allocate_pool_reach_full_arena(self)
                Tests the allocation of pools when the arena is about to be full.

            test_allocate_pool_full_arena(self)
                Tests the allocation of pools when the arena is full.

            test_allocate_pool_invalid_block_size(self)
                Tests the allocation of pools with an invalid block size.

            test_allocate_pool_max_block_size(self)
                Tests the allocation of pools with the maximum block size.

            test_allocate_pool_zero_block_size(self)
                Tests the allocation of pools with a block size of zero.

            test_allocate_block_empty(self)
                Tests the allocation of blocks when no arena or pool is allocated.

            test_allocate_block_types(self, name, obj_type)
                Tests the allocation of blocks with various object types.

            test_allocate_block_multiple_same(self)
                Tests the allocation of multiple blocks with the same object.

            test_allocate_block_multiple_different(self)
                Tests the allocation of multiple blocks with different objects.

            test_allocate(self)
                Tests the allocation of memory for an object.

            test_allocate_types(self, name, obj_type)
                Tests the allocation of memory for various object types.

            test_allocate_max_block_size(self)
                Tests the allocation of memory for an object with the maximum block size.

            test_allocate_large_block_size(self)
                Tests the allocation of memory for an object with a size that is too large.

            test_allocate_multiple_arenas(self)
                Tests the allocation of memory that requires multiple arenas.

            test_deallocate_multiple_blocks_to_empty(self)
                Tests the deallocation of multiple blocks to empty the manager.

            test_deallocate_not_empty(self)
                Tests the deallocation of a block when the manager is not empty.

            test_deallocate_non_existent_block(self)
                Tests the deallocation of a non-existent block.

            test_deallocate_from_full_pool(self)
                Tests the deallocation of a block from a full pool.

            test_deallocate_from_full_arena(self)
                Tests the deallocation of a block from a full arena.

            test_reuse_free_block(self)
                Tests the reuse of a free block.

            test_reuse_free_pool(self)
                Tests the reuse of a free pool.

            test_reuse_free_arena(self)
                Tests the reuse of a free arena.
"""

import unittest
from pympler import asizeof
from parameterized import parameterized

from manager import MemoryManager
from memory import Arena, Pool, Block

def get_types():
    """
    Returns a list of types for testing.

    Returns:
        list: A list of tuples containing the name and type.
    """
    return [
        ("string", "8"),
        ("float", 8.0),
        ("list", []),
        ("dict", {}),
        ("tuple", ()),
        ("set", set()),
        ("custom_object", Block(8)) # Test with a custom object
    ]

class TestMemoryManager(unittest.TestCase):
    """
    Unit tests for the MemoryManager class.
    """

    def setUp(self):
        """
        Sets up the test case environment.
        """
        self.manager = MemoryManager.get_instance()
        self.manager.arenas = []  # Reset the singleton instance for each test

    def test_get_instance(self):
        """
        Tests the singleton instance of the MemoryManager.
        """
        self.manager = MemoryManager.get_instance()
        self.assertIsInstance(self.manager, MemoryManager)
        self.assertEqual(self.manager, MemoryManager._instance)
        self.assertEqual(self.manager, MemoryManager.get_instance())

    def test_allocate_arena(self):
        """
        Tests the allocation of arenas.
        """
        arena1 = self.manager._allocate_arena()
        arena2 = self.manager._allocate_arena()

        self.assertIsInstance(arena1, Arena)
        self.assertIsInstance(arena2, Arena)
        self.assertEqual(self.manager.arenas, [arena1, arena2])

    def test_allocate_pool_after_arena(self):
        """
        Tests the allocation of pools after an arena is allocated.
        """
        arena = self.manager._allocate_arena()
        pool = self.manager._allocate_pool(8)

        self.assertIsInstance(pool, Pool)
        self.assertEqual(self.manager.arenas, [arena])
        self.assertEqual(self.manager.arenas[0].pools, [pool])

    def test_allocate_pool(self):
        """
        Tests the allocation of pools.
        """
        pool1 = self.manager._allocate_pool(8)
        pool2 = self.manager._allocate_pool(16)

        self.assertIsInstance(pool1, Pool)
        self.assertIsInstance(pool2, Pool)
        self.assertIsInstance(self.manager.arenas[0], Arena)  # Created automatically
        self.assertEqual(self.manager.arenas[0].pools, [pool1, pool2])

    def test_allocate_pool_reach_full_arena(self):
        """
        Tests the allocation of pools when the arena is about to be full.
        """
        arena = self.manager._allocate_arena()
        arena.bytes = 252000
        pool = self.manager._allocate_pool(8)

        self.assertIsInstance(pool, Pool)
        self.assertEqual(self.manager.arenas[0].bytes, 256000)
        self.assertEqual(len(self.manager.arenas), 1)

    def test_allocate_pool_full_arena(self):
        """
        Tests the allocation of pools when the arena is full.
        """
        arena = self.manager._allocate_arena()
        arena.bytes = 256000
        pool = self.manager._allocate_pool(8)

        self.assertIsInstance(pool, Pool)
        self.assertEqual(len(self.manager.arenas), 2)  # New arena created since the first one is full

    def test_allocate_pool_invalid_block_size(self):
        """
        Tests the allocation of pools with an invalid block size.
        """
        with self.assertRaises(ValueError):
            self.manager._allocate_pool(7)  # Not divisible by 8

    def test_allocate_pool_max_block_size(self):
        """
        Tests the allocation of pools with the maximum block size.
        """
        pool = self.manager._allocate_pool(Pool.MAXSIZE)

        self.assertIsInstance(pool, Pool)
        self.assertEqual(pool.block_size, Pool.MAXSIZE)

    def test_allocate_pool_zero_block_size(self):
        """
        Tests the allocation of pools with a block size of zero.
        """
        with self.assertRaises(ValueError):
            self.manager._allocate_pool(0)

    def test_allocate_block_empty(self):
        """
        Tests the allocation of blocks when no arena or pool is allocated.
        """
        block = self.manager._allocate_block(8)

        self.assertIsNone(block)

    @parameterized.expand(get_types())
    def test_allocate_block_types(self, name, obj_type):
        """
        Tests the allocation of blocks with various object types.

        Args:
            name (str): The name of the object type.
            obj_type (any): The object type to test.
        """
        self.manager._allocate_arena()
        self.manager._allocate_pool(asizeof.asizeof(obj_type))
        block = self.manager._allocate_block(obj_type)

        self.assertIsInstance(block, Block)
        self.assertEqual(block.obj, obj_type)
        self.assertEqual(self.manager.arenas[0].pools[0].blocks, [block])

    def test_allocate_block_multiple_same(self):
        """
        Tests the allocation of multiple blocks with the same object.
        """
        self.manager._allocate_arena()
        self.manager._allocate_pool(asizeof.asizeof(8))
        block1 = self.manager._allocate_block(8)
        block2 = self.manager._allocate_block(8)

        self.assertIsInstance(block1, Block)
        self.assertIsInstance(block2, Block)
        self.assertEqual(block1.obj, 8)
        self.assertEqual(block2.obj, 8)
        self.assertEqual(self.manager.arenas[0].pools[0].blocks, [block1, block2])

    def test_allocate_block_multiple_different(self):
        """
        Tests the allocation of multiple blocks with different objects.
        """
        self.manager._allocate_arena()
        self.manager._allocate_pool(asizeof.asizeof(8))
        self.manager._allocate_pool(asizeof.asizeof(16**100))
        block1 = self.manager._allocate_block(8)
        block2 = self.manager._allocate_block(16**100)

        self.assertIsInstance(block1, Block)
        self.assertIsInstance(block2, Block)
        self.assertEqual(self.manager.arenas[0].pools[0].blocks, [block1])
        self.assertEqual(self.manager.arenas[0].pools[1].blocks, [block2])

    def test_allocate(self):
        """
        Tests the allocation of memory for an object.
        """
        self.manager.allocate(8)

        self.assertEqual(self.manager.arenas[0].pools[0].blocks[0].obj, 8)

    @parameterized.expand(get_types())
    def test_allocate_types(self, name, obj_type):
        """
        Tests the allocation of memory for various object types.

        Args:
            name (str): The name of the object type.
            obj_type (any): The object type to test.
        """
        self.manager.allocate(obj_type)

        self.assertEqual(self.manager.arenas[0].pools[0].blocks[0].obj, obj_type)

    def test_allocate_max_block_size(self):
        """
        Tests the allocation of memory for an object with the maximum block size.
        """
        self.manager.allocate(b'x' * (512 - 40))  # 512 bytes total, -40 is to remove overhead

        # Arena, pool, and block are created, block size is 512 as it is the maximum
        self.assertEqual(self.manager.arenas[0].pools[0].blocks[0].block_size, Block.MAXSIZE)

    def test_allocate_large_block_size(self):
        """
        Tests the allocation of memory for an object with a size that is too large.
        """
        with self.assertRaises(ValueError):
            self.manager.allocate("x" * 10000)

    def test_allocate_multiple_arenas(self):
        """
        Tests the allocation of memory that requires multiple arenas.
        """
        self.manager.allocate(8)
        self.manager.arenas[0].bytes = 256000
        self.manager.allocate(8)

        self.assertEqual(len(self.manager.arenas), 2)  # New arena created for the third allocation

    def test_deallocate_multiple_blocks_to_empty(self):
        """
        Tests the deallocation of multiple blocks to empty the manager.
        """
        self.manager.allocate(8)
        self.manager.allocate(16)
        block1 = self.manager.arenas[0].pools[0].blocks[0]
        block2 = self.manager.arenas[0].pools[0].blocks[1]
        self.manager.deallocate(block1)
        self.manager.deallocate(block2)

        self.assertEqual(len(self.manager.free_blocks), 2)  # Two blocks are saved for reuse
        self.assertEqual(len(self.manager.free_pools), 1)  # The one pool is saved for reuse
        self.assertEqual(len(self.manager.free_arenas), 1)  # The one arena is saved for reuse
        self.assertEqual(len(self.manager.arenas), 0)  # Manager is empty

    def test_deallocate_not_empty(self):
        """
        Tests the deallocation of a block when the manager is not empty.
        """
        self.manager.allocate(8)
        self.manager.allocate(16)
        block = self.manager.arenas[0].pools[0].blocks[0]
        self.manager.deallocate(block)

        self.assertEqual(len(self.manager.free_blocks), 1)  # The block is saved for reuse
        self.assertEqual(len(self.manager.arenas[0].pools[0].blocks), 1) # Block, pool, & arena exist

    def test_deallocate_non_existent_block(self):
        """
        Tests the deallocation of a non-existent block.
        """
        self.manager.allocate(8)
        block = Block(16)
        result = self.manager.deallocate(block)

        self.assertFalse(result)  # Deallocation should fail
        self.assertEqual(len(self.manager.arenas[0].pools[0].blocks), 1)  # No block is removed

    def test_deallocate_from_full_pool(self):
        """
        Tests the deallocation of a block from a full pool.
        """
        self.manager.allocate(8)
        self.manager.arenas[0].pools[0].bytes = Pool.MAXSIZE
        block = self.manager.arenas[0].pools[0].blocks[0]
        self.manager.deallocate(block)

        self.assertEqual(len(self.manager.free_blocks), 1)  # Block is saved for reuse
        self.assertEqual(len(self.manager.arenas[0].pools), 1)  # Pool is not removed
        self.assertEqual(len(self.manager.arenas[0].pools[0].blocks), 0)  # Block is removed

    def test_deallocate_from_full_arena(self):
        """
        Tests the deallocation of a block from a full arena.
        """
        self.manager.allocate(8)
        self.manager.arenas[0].bytes = Arena.MAXSIZE
        block = self.manager.arenas[0].pools[0].blocks[0]
        self.manager.deallocate(block)

        self.assertEqual(len(self.manager.free_blocks), 1)  # Block is saved for reuse
        self.assertEqual(len(self.manager.free_pools), 1)  # Pool is saved for reuse
        self.assertEqual(len(self.manager.arenas), 1)  # Arena is not removed

    def test_reuse_free_block(self):
        """
        Tests the reuse of a free block.
        """
        self.manager.allocate("object 1")
        block1 = self.manager.arenas[0].pools[0].blocks[0]
        self.manager.deallocate(block1)
        self.manager.allocate("object 2")
        block2 = self.manager.arenas[0].pools[0].blocks[0]

        self.assertIs(block1.obj, block2.obj) # The same block is reused

    def test_reuse_free_pool(self):
        """
        Tests the reuse of a free pool.
        """
        self.manager.allocate("object 1")
        pool1 = self.manager.arenas[0].pools[0]
        block1 = pool1.blocks[0]
        self.manager.deallocate(block1)
        self.manager.allocate("object 2")
        pool2 = self.manager.arenas[0].pools[0]

        self.assertIs(pool1, pool2) # The same pool is reused

    def test_reuse_free_arena(self):
        """
        Tests the reuse of a free arena.
        """
        self.manager.allocate("object 1")
        arena1 = self.manager.arenas[0]
        block1 = arena1.pools[0].blocks[0]
        self.manager.deallocate(block1)
        self.manager.allocate("object 2")
        arena2 = self.manager.arenas[0]

        self.assertIs(arena1, arena2) # The same arena is reused


if __name__ == '__main__':
    unittest.main()
