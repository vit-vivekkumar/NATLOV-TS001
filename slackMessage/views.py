import requests
import logging

# Initialize logger
logger = logging.getLogger(__name__)


SLACK_CHANNEL = "#all-natlov-ts001"
WEBHOOK_URL = (
    "https://hooks.slack.com/services/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"
)

def send_slack_message(user_id, effect, message):
    """
    Sends a Slack message using webhook URL.

    Args:
        user_id (str): The ID of the user.
        effect (str): The effect to display in the message.
        message (str): The message content.

    Returns:
        None
    """
    full_message = f"Effect: {effect}\nUser ID: {user_id}\nMessage: {message}"
    try:
        webhook_payload = {
            "channel": SLACK_CHANNEL,
            "text": full_message,
            "username": "Natlov - College System",
            "icon_emoji": ":warning:",
        }
        webhook_response = requests.post(WEBHOOK_URL, json=webhook_payload)
        if webhook_response.status_code == 200:
            logger.info("Message sent successfully via webhook.")
        else:
            logger.error(
                f"Failed to send message via webhook: {webhook_response.status_code} - {webhook_response.text}"
            )
    except Exception as webhook_exception:
        logger.error(f"Error using webhook: {webhook_exception}")
