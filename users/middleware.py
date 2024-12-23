from django.http import JsonResponse
from slackMessage.models import SlackMessage
from slackMessage.views import send_slack_message


class UnauthorizedRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 401:
            user_id = request.user.id if request.user.is_authenticated else None
            effect = "Unauthorized Access"
            message = f"Unauthorized request to {request.path}."
            send_slack_message(user_id, effect, message)
            SlackMessage.objects.create(
                user_id=user_id or 0, effect=effect, message=message
            )
        return response
