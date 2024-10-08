"""
NAME
    analyzer

DESCRIPTION
    This module provides the MemoryAnalyzer class for analyzing and tracking memory usage of Python objects.
    The MemoryAnalyzer class is implemented as a singleton.

CLASSES
    MemoryAnalyzer
        A singleton class used to analyze and track memory usage of Python objects.

        Methods defined here:
            get_instance() -> MemoryAnalyzer
                Returns the singleton instance of the MemoryAnalyzer.

            measure_size(self, obj)
                Measures the size of a given object.

            track(self)
                Tracks memory usage and logs the differences.

            analyze(self)
                Analyzes all objects in memory and logs the total number.

            summarize(self)
                Summarizes memory usage and logs the summary.
"""

from pympler import asizeof, tracker, muppy, summary
import logging

class MemoryAnalyzer:
    """
    A singleton class used to analyze and track memory usage of Python objects.

    Attributes:
        _instance (MemoryAnalyzer): The singleton instance of the MemoryAnalyzer.
        tracker (SummaryTracker): An instance of SummaryTracker to track memory usage.

    Methods:
        get_instance() -> MemoryAnalyzer:
            Returns the singleton instance of the MemoryAnalyzer.
        measure_size(obj):
            Measures the size of a given object.
        track():
            Tracks memory usage and logs the differences.
        analyze():
            Analyzes all objects in memory and logs the total number.
        summarize():
            Summarizes memory usage and logs the summary.
    """
    _instance = None

    def __init__(self, log_file='memory_log.txt'):
        """
        Initializes the MemoryAnalyzer with a log file.

        Args:
            log_file (str): The name of the log file. Default is 'memory_log.txt'.

        Raises:
            Exception: If an instance of MemoryAnalyzer already exists.
        """
        if MemoryAnalyzer._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.tracker = tracker.SummaryTracker()
            logging.basicConfig(
                filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s'
            )
            MemoryAnalyzer._instance = self

    @staticmethod
    def get_instance(log_file='memory_log.txt'):
        """
        Returns the singleton instance of the MemoryAnalyzer.

        Args:
            log_file (str): The name of the log file. Default is 'memory_log.txt'.

        Returns:
            MemoryAnalyzer: The singleton instance of the MemoryAnalyzer.
        """
        if MemoryAnalyzer._instance is None:
            MemoryAnalyzer(log_file)
        return MemoryAnalyzer._instance

    def measure_size(self, obj):
        """
        Measures the size of a given object.

        Args:
            obj (object): The object to measure.

        Returns:
            int: The size of the object in bytes.
        """
        size = asizeof.asizeof(obj)
        logging.info(f"Size of object: {size} bytes\n")
        return size

    def track(self):
        """
        Tracks memory usage and logs the differences.
        """
        diff = self.tracker.diff()
        logging.info("Track:")
        for entry in diff:
            logging.info(f"Type: {entry[0]}, Count: {entry[1]}, Size: {entry[2]} bytes")

    def analyze(self):
        """
        Analyzes all objects in memory and logs the total number.

        Returns:
            list: A list of all objects in memory.
        """
        all_objects = muppy.get_objects()
        logging.info(f"Total number of objects: {len(all_objects)}\n")
        return all_objects

    def summarize(self):
        """
        Summarizes memory usage and logs the summary.

        Returns:
            list: A summary of memory usage.
        """
        all_objects = self.analyze()
        sum_list = summary.summarize(all_objects)
        logging.info("Summarize:")
        # summ
        for entry in sum_list:
            logging.info(f"Type: {entry[0]}, Count: {entry[1]}, Size: {entry[2]} bytes")
        return sum_list
