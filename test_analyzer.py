import unittest
from unittest.mock import patch, MagicMock
import logging
from analyzer import MemoryAnalyzer

class TestMemoryAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = MemoryAnalyzer(log_file='test_log.txt')

    @patch('analyzer.logging.basicConfig')
    @patch('analyzer.tracker.SummaryTracker')
    def test_init(self, mock_tracker, mock_basicConfig):
        analyzer = MemoryAnalyzer(log_file='test_log.txt')
        mock_tracker.assert_called_once()
        mock_basicConfig.assert_called_once_with(
            filename='test_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s'
        )

    @patch('analyzer.logging.info')
    @patch('pympler.asizeof.asizeof', return_value=100)
    def test_measure_size(self, mock_asizeof, mock_logging_info):
        size = self.analyzer.measure_size("object")
        mock_asizeof.assert_called_once_with("object")
        mock_logging_info.assert_called_once_with("Size of object: 100 bytes\n")
        self.assertEqual(size, 100)

    @patch('analyzer.logging.info')
    @patch('analyzer.tracker.SummaryTracker.diff', return_value=[('list', 1, 100)])
    def test_track(self, mock_diff, mock_logging_info):
        self.analyzer.track()
        mock_diff.assert_called_once()
        mock_logging_info.assert_any_call("Track:")
        mock_logging_info.assert_any_call("Type: list, Count: 1, Size: 100 bytes")

    @patch('analyzer.logging.info') 
    @patch('pympler.muppy.get_objects', return_value=['obj1', 'obj2'])
    def test_analyze(self, mock_get_objects, mock_logging_info):
        all_objects = self.analyzer.analyze()
        mock_get_objects.assert_called_once()
        mock_logging_info.assert_called_once_with("Total number of objects: 2\n")
        self.assertEqual(all_objects, ['obj1', 'obj2'])

    @patch('analyzer.logging.info')
    @patch('analyzer.MemoryAnalyzer.analyze', return_value=['obj1', 'obj2'])
    @patch('pympler.summary.summarize', return_value=[('list', 1, 5000), ('dict', 2, 3000)])
    def test_summarize(self, mock_summarize, mock_analyze_memory, mock_logging_info):
        summary = self.analyzer.summarize()
        mock_analyze_memory.assert_called_once()
        mock_summarize.assert_called_once_with(['obj1', 'obj2'])
        mock_logging_info.assert_any_call("Summarize:")
        mock_logging_info.assert_any_call("Type: list, Count: 1, Size: 5000 bytes")
        mock_logging_info.assert_any_call("Type: dict, Count: 2, Size: 3000 bytes")
        self.assertEqual(summary, [('list', 1, 5000), ('dict', 2, 3000)])

if __name__ == '__main__':
    unittest.main()
