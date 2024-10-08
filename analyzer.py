from pympler import asizeof, tracker, muppy, summary
import logging

class MemoryAnalyzer:
    """A class used to analyze and track memory usage of Python objects."""

    def __init__(self, log_file='memory_log.txt'):
        self.tracker = tracker.SummaryTracker()
        logging.basicConfig(
            filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s'
        )

    def measure_size(self, obj):
        size = asizeof.asizeof(obj)
        logging.info(f"Size of object: {size} bytes\n")
        return size

    def track(self):
        diff = self.tracker.diff()
        logging.info("Track:")
        for entry in diff:
            logging.info(f"Type: {entry[0]}, Count: {entry[1]}, Size: {entry[2]} bytes")

    def analyze(self):
        all_objects = muppy.get_objects()
        logging.info(f"Total number of objects: {len(all_objects)}\n")
        return all_objects

    def summarize(self):
        all_objects = self.analyze()
        sum_list = summary.summarize(all_objects)
        logging.info("Summarize:")
        for entry in sum_list:
            logging.info(f"Type: {entry[0]}, Count: {entry[1]}, Size: {entry[2]} bytes")
        return sum_list
