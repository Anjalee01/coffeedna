import unittest
import os
import json
from backend.chat_history import load_history, save_history

class TestChatHistory(unittest.TestCase):
    test_user_id = "test_user"
    test_data_folder = "data"
    test_history_file = os.path.join(test_data_folder, f"{test_user_id}_history.json")

    def setUp(self):
        # Ensure test environment setup by clearing any existing history file
        if os.path.exists(self.test_history_file):
            os.remove(self.test_history_file)

    def tearDown(self):
        # Clean up test file after each test
        if os.path.exists(self.test_history_file):
            os.remove(self.test_history_file)

    def test_load_history_empty(self):
        # Load history for a new user (no file should exist)
        history = load_history(self.test_user_id)
        self.assertEqual(history, [])

    def test_save_and_load_history(self):
        # Save a new message and check if it loads correctly
        test_message = {"role": "user", "content": "Test message"}
        save_history(self.test_user_id, test_message)
        
        history = load_history(self.test_user_id)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0], test_message)

if __name__ == "__main__":
    unittest.main()
