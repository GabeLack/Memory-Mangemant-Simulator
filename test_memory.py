import unittest
from pympler import asizeof
from parameterized import parameterized

from memory import Arena, Pool, Block

def get_invalid_types():
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

    def test_arena(self):
        a = Arena()
        self.assertEqual(a.pools, [])
        self.assertEqual(a.bytes, 0)

    def test_check_arena_empty(self):
        a = Arena()
        # 4000 being the full/max pool size
        self.assertTrue(a.check_arena(4000))

    def test_check_arena_reach_full(self):
        a = Arena()
        a.bytes = 252000
        self.assertTrue(a.check_arena(4000))

    def test_check_arena_full(self):
        a = Arena()
        a.bytes = 256000
        self.assertFalse(a.check_arena(4000))

    @parameterized.expand(get_invalid_types())
    def test_check_arena_invalid_pool_size_type(self, name, invalid_type):
        a = Arena()
        with self.assertRaises(TypeError):
            a.check_arena(invalid_type)


class TestPool(unittest.TestCase):
    def test_pool(self):
        p = Pool(8)
        self.assertEqual(p.blocks, [])
        self.assertEqual(p.bytes, 0)
        self.assertEqual(p.block_size, 8)

    def test_pool_invalid_block_size(self):
        # 7 is not divisible by 8
        with self.assertRaises(ValueError):
            Pool(10)

    @parameterized.expand(get_invalid_types())
    def test_pool_invalid_block_size_type(self, name, invalid_type):
        with self.assertRaises(TypeError):
            Pool(invalid_type)

    def test_pool_invalid_block_size_zero(self):
        with self.assertRaises(ValueError):
            Pool(0)

    def test_check_pool(self):
        p = Pool(8)
        self.assertTrue(p.check_pool(8))
        self.assertFalse(p.check_pool(16))

    def test_check_pool_reach_full(self):
        p = Pool(8)
        p.bytes = 3992
        self.assertTrue(p.check_pool(8))

    def test_check_pool_full(self):
        p = Pool(8)
        p.bytes = 4000
        self.assertFalse(p.check_pool(8))


class TestBlock(unittest.TestCase):
    @parameterized.expand(get_invalid_types())
    def test_block_types(self, name, obj_type):
        b = Block(obj_type)
        self.assertEqual(b.obj, obj_type)
        self.assertEqual(b.block_size, asizeof.asizeof(obj_type))

    def test_block_size_max_size(self):
        Block(b'x' * 472) # + 40 bytes overhead = 512 bytes total
        self.assertEqual(Block.MAXSIZE, 512)

    def test_block_size_too_large(self):
        with self.assertRaises(ValueError):
            Block(b'x' * 512) # + 40 bytes overhead


if __name__ == '__main__':
    unittest.main()
