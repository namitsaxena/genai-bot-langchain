import unittest
import json

class MyTestCase(unittest.TestCase):
    def test_json(self):
        json_str = '{"action": "Final Answer", "action_input": "I can help you with a variety of tasks, including scheduling jobs, checking the status of jobs, and interacting with Kubernetes clusters."}'
        jsn = json.loads(json_str)
        if "action_input" in jsn:
            print("Output:-" + jsn["action_input"])
        else:
            print("key not found")
        # self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
