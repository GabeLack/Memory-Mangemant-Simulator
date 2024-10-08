import time
import random
import threading
from manager import MemoryManager
from analyzer import MemoryAnalyzer

def allocate_blocks(manager, duration=30):
    """
    Continuously allocates blocks of random sizes using the MemoryManagerfor the
    specified duration.

    Args:
        manager (MemoryManager): The memory manager instance.
        duration (int): The duration for which to run the allocation in seconds.
            Default is 60 seconds.
    """
    start_time = time.time()
    while time.time() - start_time < duration:
        block_size = random.randint(100, 300)  # Random block size between 1 and 512 bytes
        obj = bytearray(block_size)  # Create a dummy object of the specified size
        manager.allocate(obj)
        time.sleep(0.01)  # Sleep for a short duration to simulate work

def run_analyzer(analyzer, duration=30):
    """
    Runs the MemoryAnalyzer to track memory usage during the specified duration.

    Args:
        analyzer (MemoryAnalyzer): The memory analyzer instance.
        duration (int): The duration for which to run the analyzer in seconds.
            Default is 60 seconds.
    """
    start_time = time.time()
    while time.time() - start_time < duration:
        analyzer.track()
        time.sleep(5)  # Track memory usage every 5 seconds

if __name__ == "__main__":
    manager = MemoryManager.get_instance()
    analyzer = MemoryAnalyzer.get_instance(log_file='memory_log.txt')

    # Create threads for allocation and analysis
    allocation_thread = threading.Thread(target=allocate_blocks, args=(manager,))
    analyzer_thread = threading.Thread(target=run_analyzer, args=(analyzer,))

    # Start the threads
    allocation_thread.start()
    analyzer_thread.start()

    # Wait for the threads to complete
    allocation_thread.join()
    analyzer_thread.join()

    # Summarize memory usage at the end
    analyzer.summarize()

    # Key output from the memory_log.txt file:
    # 2024-10-08 23:42:36,145 - Type: memory.Arena, Count: 3, Size: 144 bytes
    # 2024-10-08 23:42:36,145 - Type: memory.Pool, Count: 157, Size: 7536 bytes
    # 2024-10-08 23:42:36,145 - Type: memory.Block, Count: 1861, Size: 89328 bytes
