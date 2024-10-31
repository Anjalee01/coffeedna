import unittest
from unittest.mock import patch, MagicMock
from backend.chat_logic import get_coffee_recommendation

class TestChatLogic(unittest.TestCase):
    @patch("backend.chat_logic.client.chat.completions.create")
    def test_get_coffee_recommendation(self, mock_create):
        # Mock OpenAI response
        mock_create.return_value = MagicMock(choices=[MagicMock(message=MagicMock(content="Sample coffee recommendation response"))])

        # Define test inputs
        user_id = "test_user"
        user_input = "I'd like a smooth coffee with a hint of chocolate."
        user_preferences = {
            "language": "English",
            "tone": "friendly",
            "detail_level": "concise"
        }

        # Run the function
        response = get_coffee_recommendation(user_id, user_input, user_preferences)

        # Assert the response matches the mock
        self.assertEqual(response, "Sample coffee recommendation response")

        # Check if OpenAI API was called and how many times
        self.assertGreaterEqual(mock_create.call_count, 1, "Expected at least one call to OpenAI API")

        # Optionally: Check if the last call was with the expected parameters
        last_call_args = mock_create.call_args_list[-1]
        self.assertIn("gpt-4o", last_call_args[1]["model"])  # Check if the model is correct

if __name__ == "__main__":
    unittest.main()
