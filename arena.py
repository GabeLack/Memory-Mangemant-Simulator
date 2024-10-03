# simulate the arena of memory

class Arena:
    MAXSIZE = 256000

    def __init__(self):
        self.pools = []
        self.bytes = 0
        self.free = True

    def check_arena(self, pool_size):
        # Check if adding the new pool would exceed the maximum size
        return self.bytes + pool_size <= self.MAXSIZE
