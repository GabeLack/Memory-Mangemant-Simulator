"""
NAME
    test_memory

DESCRIPTION
    This module contains unit tests for the memory management classes: Arena, Pool, and Block.
    It uses the unittest framework and parameterized tests for various invalid types.

CLASSES
    TestArena
        Unit tests for the Arena class.

        Methods defined here:
            test_arena(self)
                Tests the initialization of the Arena class.

            test_check_arena_empty(self)
                Tests the check_arena method when the arena is empty.

            test_check_arena_reach_full(self)
                Tests the check_arena method when the arena is about to be full.

            test_check_arena_full(self)
                Tests the check_arena method when the arena is full.

            test_check_arena_invalid_pool_size_type(self, name, invalid_type)
                Tests the check_arena method with invalid pool size types.

    TestPool
        Unit tests for the Pool class.

        Methods defined here:
            test_pool(self)
                Tests the initialization of the Pool class.

            test_pool_invalid_block_size(self)
                Tests the Pool class with an invalid block size.

            test_pool_invalid_block_size_type(self, name, invalid_type)
                Tests the Pool class with invalid block size types.

            test_pool_invalid_block_size_zero(self)
                Tests the Pool class with a block size of zero.

            test_check_pool(self)
                Tests the check_pool method.

            test_check_pool_reach_full(self)
                Tests the check_pool method when the pool is about to be full.

            test_check_pool_full(self)
                Tests the check_pool method when the pool is full.

    TestBlock
        Unit tests for the Block class.

        Methods defined here:
            test_block_types(self, name, obj_type)
                Tests the Block class with various object types.

            test_block_size_max_size(self)
                Tests the Block class with the maximum block size.

            test_block_size_too_large(self)
                Tests the Block class with an object size that is too large.
"""

import unittest
from pympler import asizeof
from parameterized import parameterized

from memory import Arena, Pool, Block

def get_invalid_types():
    """
    Returns a list of invalid types for testing.

    Returns:
        list: A list of tuples containing the name and invalid type.
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


class TestArena(unittest.TestCase):
    """
    Unit tests for the Arena class.
    """

    def test_arena(self):
        """
        Tests the initialization of the Arena class.
        """
        a = Arena()
        self.assertEqual(a.pools, [])
        self.assertEqual(a.bytes, 0)

    def test_check_arena_empty(self):
        """
        Tests the check_arena method when the arena is empty.
        """
        a = Arena()
        # 4000 being the full/max pool size
        self.assertTrue(a.check_arena(4000))

    def test_check_arena_reach_full(self):
        """
        Tests the check_arena method when the arena is about to be full.
        """
        a = Arena()
        a.bytes = 252000
        self.assertTrue(a.check_arena(4000))

    def test_check_arena_full(self):
        """
        Tests the check_arena method when the arena is full.
        """
        a = Arena()
        a.bytes = 256000
        self.assertFalse(a.check_arena(4000))

    @parameterized.expand(get_invalid_types())
    def test_check_arena_invalid_pool_size_type(self, name, invalid_type):
        """
        Tests the check_arena method with invalid pool size types.

        Args:
            name (str): The name of the invalid type.
            invalid_type (any): The invalid type to test.
        """
        a = Arena()
        with self.assertRaises(TypeError):
            a.check_arena(invalid_type)


class TestPool(unittest.TestCase):
    """
    Unit tests for the Pool class.
    """

    def test_pool(self):
        """
        Tests the initialization of the Pool class.
        """
        p = Pool(8)
        self.assertEqual(p.blocks, [])
        self.assertEqual(p.bytes, 0)
        self.assertEqual(p.block_size, 8)

    def test_pool_invalid_block_size(self):
        """
        Tests the Pool class with an invalid block size.
        """
        # 7 is not divisible by 8
        with self.assertRaises(ValueError):
            Pool(10)

    @parameterized.expand(get_invalid_types())
    def test_pool_invalid_block_size_type(self, name, invalid_type):
        """
        Tests the Pool class with invalid block size types.

        Args:
            name (str): The name of the invalid type.
            invalid_type (any): The invalid type to test.
        """
        with self.assertRaises(TypeError):
            Pool(invalid_type)

    def test_pool_invalid_block_size_zero(self):
        """
        Tests the Pool class with a block size of zero.
        """
        with self.assertRaises(ValueError):
            Pool(0)

    def test_check_pool(self):
        """
        Tests the check_pool method.
        """
        p = Pool(8)
        self.assertTrue(p.check_pool(8))
        self.assertFalse(p.check_pool(16))

    def test_check_pool_reach_full(self):
        """
        Tests the check_pool method when the pool is about to be full.
        """
        p = Pool(8)
        p.bytes = 3992
        self.assertTrue(p.check_pool(8))

    def test_check_pool_full(self):
        """
        Tests the check_pool method when the pool is full.
        """
        p = Pool(8)
        p.bytes = 4000
        self.assertFalse(p.check_pool(8))


class TestBlock(unittest.TestCase):
    """
    Unit tests for the Block class.
    """

    @parameterized.expand(get_invalid_types())
    def test_block_types(self, name, obj_type):
        """
        Tests the Block class with various object types.

        Args:
            name (str): The name of the object type.
            obj_type (any): The object type to test.
        """
        b = Block(obj_type)
        self.assertEqual(b.obj, obj_type)
        self.assertEqual(b.block_size, asizeof.asizeof(obj_type))

    def test_block_size_max_size(self):
        """
        Tests the Block class with the maximum block size.
        """
        Block(b'x' * 472) # + 40 bytes overhead = 512 bytes total
        self.assertEqual(Block.MAXSIZE, 512)

    def test_block_size_too_large(self):
        """
        Tests the Block class with an object size that is too large.
        """
        with self.assertRaises(ValueError):
            Block(b'x' * 512) # + 40 bytes overhead


if __name__ == '__main__':
    unittest.main()
