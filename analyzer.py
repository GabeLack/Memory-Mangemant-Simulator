from pympler import asizeof, tracker, muppy, summary
import logging

class MemoryAnalyzer:
    """A class used to analyze and track memory usage of Python objects."""

    @staticmethod
    def initialize(log_file='memory_log.txt'):
        """
        Initializes the MemoryAnalyzer with a log file.

        Args:
            log_file (str): The name of the log file to write memory usage information to.
        """
        MemoryAnalyzer.tracker = tracker.SummaryTracker()
        logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

    @staticmethod
    def measure_size(obj):
        """
        Measures the size of a given object.

        Args:
            obj: The object to measure the size of.

        Returns:
            int: The size of the object in bytes.
        """
        size = asizeof.asizeof(obj)
        logging.info(f"Size of object: {size} bytes\n")
        return size

    @staticmethod
    def track_memory():
        """
        Tracks the memory usage and logs the differences.
        """
        diff = MemoryAnalyzer.tracker.diff()
        logging.info("Track:")
        for line in diff:
            logging.info(f"Type: {line[0]}, Count: {line[1]}, Size: {line[2]} bytes")

    @staticmethod
    def analyze_memory():
        """
        Analyzes the current memory usage.

        Returns:
            list: A list of all objects currently in memory.
        """
        all_objects = muppy.get_objects()
        logging.info(f"Total number of objects: {len(all_objects)}\n")
        return all_objects

    @staticmethod
    def summarize_memory():
        """
        Summarizes the memory usage of all objects.

        Returns:
            list: A summary of memory usage by object type.
        """
        all_objects = MemoryAnalyzer.analyze_memory()
        sum1 = summary.summarize(all_objects)
        logging.info("Summarize:")
        for item in sum1:
            if item[0] in ["pool.Pool", "arena.Arena", "block.Block"]:
                logging.info(f"Type: {item[0]}, Count: {item[1]}, Size: {item[2]} bytes")
            elif item[2] > 4096: # if the size is greater than 4KB
                logging.info(f"Type: {item[0]}, Count: {item[1]}, Size: {item[2]} bytes")
        return sum1
