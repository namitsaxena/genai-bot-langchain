import unittest

from src.utils.GCPLoggingUtility import GCPCloudLoggingUtility


class TestGCPLoggingUtility(unittest.TestCase):
    def setUp(self):
        self.util = GCPCloudLoggingUtility()

    def test_log_retriever(self):
        entries = self.util.retrieve_logs()
        for entry in entries:
            print(entry)