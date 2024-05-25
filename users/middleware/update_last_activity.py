from django.http import HttpRequest
from django.http import HttpResponse
from django.utils.timezone import now


class UpdateLastActivityMiddleware:
    def __init__(self, get_response: callable) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)

        if request.user.is_authenticated:
            time_delta = now() - request.user.last_activity
            if time_delta.total_seconds() >= 600:
                request.user.last_activity = now()
                request.user.save(update_fields=["last_activity"])

        return response
