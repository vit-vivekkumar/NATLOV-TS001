from django.test import TestCase

# Create your tests here.
from unittest.mock import patch
from django.test import TestCase
from your_app_name.slack import send_slack_message

class SlackIntegrationTest(TestCase):
    @patch('your_app_name.slack.send_slack_message')
    def test_send_slack_message_called(self, mock_send_slack_message):
        # Call the function
        send_slack_message(user_id=1, effect="Test Effect", message="Test Message")
        
        # Verify it was called with the correct parameters
        mock_send_slack_message.assert_called_once_with(user_id=1, effect="Test Effect", message="Test Message")
