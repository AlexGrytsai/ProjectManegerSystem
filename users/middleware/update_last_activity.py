from django.http import HttpRequest, HttpResponseRedirect
from django.utils.timezone import now


class UpdateLastActivityMiddleware:
    def __init__(self, get_response: callable) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponseRedirect:
        response = self.get_response(request)

        if request.user.is_authenticated:
            request.user.last_activity = now()
            request.user.save(update_fields=["last_activity"])

        return response
