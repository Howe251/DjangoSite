from django.contrib.auth import backends


class MultAuthBackend(backends.ModelBackend):
    def user_can_authenticate(self, user):
        return True
