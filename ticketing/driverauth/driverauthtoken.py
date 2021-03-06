import base64

from itsdangerous import Signer

from tessera import settings

from ticketing.models import Driver
from itsdangerous import BadSignature
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import authentication
from rest_framework import exceptions


class BadTokenError(Exception):
    pass


class DriverAuth:

    def __init__(self, secret_key=settings.SECRET_KEY):
        if secret_key is None:
            raise Exception("secret key not set")

        self.s = Signer(secret_key)

    def createtoken(self, id):
        token = self.s.sign(str(id).encode())
        return base64.b64encode(token).decode('UTF-8')

    def verifytoken(self, token):
        """Returns if the token is valid otherwise, returns throws does not
        exist exception """
        try:
            bytesToken = base64.b64decode(token.encode())
            id = self.s.unsign(bytesToken)
            driver = Driver.objects.get(pk=id)
            return driver
        except (ObjectDoesNotExist, BadSignature):
            raise BadTokenError()


class DriverAuthenticate(authentication.BaseAuthentication):
    """
    Header must be X-DRIVER-TOKEN
    """

    def authenticate(self, request):
        token = request.META.get("HTTP_X_DRIVER_TOKEN")
        if not token:
            return None
        try:
            driver = DriverAuth().verifytoken(token)
            return driver, None
        except BadTokenError:
            raise exceptions.AuthenticationFailed("Bad Token Error")
