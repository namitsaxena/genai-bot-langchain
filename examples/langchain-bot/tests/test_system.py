import unittest
import subprocess

from src.utils.SystemUtility import SystemUtility


class TestSystem(unittest.TestCase):
    def setUp(self):
        self.sys = SystemUtility()

    def test_simple_command_string(self):
        output = self.sys.run_command("ls -l")
        print("Output:-\n" + output)
        assert "total" in output

    def test_simple_command_list(self):
        output = self.sys.run_command(["ls", "-l"])
        print("Output:-\n" + output)
        assert "total" in output

    def test_kubernetes_command(self):
        output = self.sys.run_command(["kubectl", "config", "view"])
        print("Output:-\n" + output)
        assert "cluster" in output

    def test_timeout_error(self):
        # verify that timeout exception gets thrown
        with self.assertRaises(subprocess.TimeoutExpired) as context:
            output = self.sys.run_command(["sleep", "30"], 2)
            # these don't matter
            # print("Output:-\n" + str(output))
            # assert "timed out" in output
