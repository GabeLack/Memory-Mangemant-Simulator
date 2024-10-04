from arena import Arena
import unittest

class TestArena(unittest.TestCase):
    def test_arena(self):
        a = Arena()
        self.assertEqual(a.pools, [])
        self.assertEqual(a.bytes, 0)
        self.assertTrue(a.free)

    def test_check_arena(self):
        a = Arena()
        self.assertTrue(a.check_arena(1000))
        self.assertTrue(a.check_arena(100000))
        self.assertFalse(a.check_arena(256001))
        self.assertFalse(a.check_arena(256000))

if __name__ == '__main__':
    unittest.main()
