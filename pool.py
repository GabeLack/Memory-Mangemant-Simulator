# simulate a pool of memory

class Pool:
    MAXSIZE = 4000

    def __init__(self, block_size):
        self.blocks = []
        self.bytes = 0
        self.block_size = block_size
        self.free = True

    def check_pool(self, block_size):
        return self.bytes + block_size <= self.MAXSIZE and self.block_size == block_size
