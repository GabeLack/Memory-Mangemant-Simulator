"""
NAME
    test_analyzer

DESCRIPTION
    This module contains unit tests for the MemoryAnalyzer class.
    It uses the unittest framework and mocks for various methods and attributes.

CLASSES
    TestMemoryAnalyzer
        Unit tests for the MemoryAnalyzer class.

        Methods defined here:
            setUp(self)
                Sets up the test case environment.

            test_get_instance(self)
                Tests the singleton instance of the MemoryAnalyzer.

            test_init(self, mock_tracker, mock_basicConfig)
                Tests the initialization of the MemoryAnalyzer.

            test_measure_size(self, mock_asizeof, mock_logging_info)
                Tests the measure_size method of the MemoryAnalyzer.

            test_track(self, mock_diff, mock_logging_info)
                Tests the track method of the MemoryAnalyzer.

            test_analyze(self, mock_get_objects, mock_logging_info)
                Tests the analyze method of the MemoryAnalyzer.

            test_summarize(self, mock_summarize, mock_analyze_memory, mock_logging_info)
                Tests the summarize method of the MemoryAnalyzer.
"""

import unittest
from unittest.mock import patch, MagicMock
import logging
from analyzer import MemoryAnalyzer

class TestMemoryAnalyzer(unittest.TestCase):
    """
    Unit tests for the MemoryAnalyzer class.
    """

    def setUp(self):
        """
        Sets up the test case environment.
        """
        # Reset the singleton instance before each test
        MemoryAnalyzer._instance = None
        self.analyzer = MemoryAnalyzer.get_instance(log_file='test_log.txt')

    def test_get_instance(self):
        """
        Tests the singleton instance of the MemoryAnalyzer.
        """
        self.assertIsInstance(self.analyzer, MemoryAnalyzer)
        self.assertEqual(self.analyzer, MemoryAnalyzer._instance)
        self.assertEqual(self.analyzer, MemoryAnalyzer.get_instance())

    @patch('analyzer.logging.basicConfig')
    @patch('analyzer.tracker.SummaryTracker')
    def test_init(self, mock_tracker, mock_basicConfig):
        """
        Tests the initialization of the MemoryAnalyzer.

        Args:
            mock_tracker (MagicMock): Mock for SummaryTracker.
            mock_basicConfig (MagicMock): Mock for logging.basicConfig.
        """
        MemoryAnalyzer._instance = None  # Reset the singleton instance
        analyzer = MemoryAnalyzer.get_instance(log_file='test_log.txt')
        mock_tracker.assert_called_once()
        mock_basicConfig.assert_called_once_with(
            filename='test_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s'
        )

    @patch('analyzer.logging.info')
    @patch('pympler.asizeof.asizeof', return_value=100)
    def test_measure_size(self, mock_asizeof, mock_logging_info):
        """
        Tests the measure_size method of the MemoryAnalyzer.

        Args:
            mock_asizeof (MagicMock): Mock for asizeof.asizeof.
            mock_logging_info (MagicMock): Mock for logging.info.
        """
        size = self.analyzer.measure_size("object")
        mock_asizeof.assert_called_once_with("object")
        mock_logging_info.assert_called_once_with("Size of object: 100 bytes\n")
        self.assertEqual(size, 100)

    @patch('analyzer.logging.info')
    @patch('analyzer.tracker.SummaryTracker.diff', return_value=[('list', 1, 100)])
    def test_track(self, mock_diff, mock_logging_info):
        """
        Tests the track method of the MemoryAnalyzer.

        Args:
            mock_diff (MagicMock): Mock for SummaryTracker.diff.
                Return value is a list of a tuple.
            mock_logging_info (MagicMock): Mock for logging.info.
        """
        self.analyzer.track()
        mock_diff.assert_called_once()
        mock_logging_info.assert_any_call("Track:")
        mock_logging_info.assert_any_call("Type: list, Count: 1, Size: 100 bytes")

    @patch('analyzer.logging.info') 
    @patch('pympler.muppy.get_objects', return_value=['obj1', 'obj2'])
    def test_analyze(self, mock_get_objects, mock_logging_info):
        """
        Tests the analyze method of the MemoryAnalyzer.

        Args:
            mock_get_objects (MagicMock): Mock for muppy.get_objects.
                Return value is a list of objects.
            mock_logging_info (MagicMock): Mock for logging.info.
        """
        all_objects = self.analyzer.analyze()
        mock_get_objects.assert_called_once()
        mock_logging_info.assert_called_once_with("Total number of objects: 2\n")
        self.assertEqual(all_objects, ['obj1', 'obj2'])

    @patch('analyzer.logging.info')
    @patch('analyzer.MemoryAnalyzer.analyze', return_value=['obj1', 'obj2'])
    @patch('pympler.summary.summarize', return_value=[('list', 1, 5000), ('dict', 2, 3000)])
    def test_summarize(self, mock_summarize, mock_analyze_memory, mock_logging_info):
        """
        Tests the summarize method of the MemoryAnalyzer.

        Args:
            mock_summarize (MagicMock): Mock for summary.summarize.
            mock_analyze_memory (MagicMock): Mock for MemoryAnalyzer.analyze.
            mock_logging_info (MagicMock): Mock for logging.info.
        """
        summary = self.analyzer.summarize()
        mock_analyze_memory.assert_called_once()
        mock_summarize.assert_called_once_with(['obj1', 'obj2'])
        mock_logging_info.assert_any_call("Summarize:")
        mock_logging_info.assert_any_call("Type: list, Count: 1, Size: 5000 bytes")
        mock_logging_info.assert_any_call("Type: dict, Count: 2, Size: 3000 bytes")
        self.assertEqual(summary, [('list', 1, 5000), ('dict', 2, 3000)])

if __name__ == '__main__':
    unittest.main()
