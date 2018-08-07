import base64

from itsdangerous import Signer
from rest_framework.authentication import BaseAuthentication

from tessera import settings

from ticketing.models import Driver
from itsdangerous import BadSignature
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import authentication
from rest_framework import exceptions


class BadTokenError(Exception):
    pass


class DriverAuth():

    def __init__(self):
        if settings.SECRET_KEY is None:
            raise Exception("secret key not set")
        self.s = Signer(settings.SECRET_KEY)

    def createtoken(self, id):
        token = self.s.sign(str(id).encode())
        return base64.b64encode(token).decode('UTF-8')

    def verifytoken(self, token):
        """Returns if the token is valid otherwise, returns throws does not exist exception"""
        try:
            bytesToken = base64.b64decode(token.encode())
            id = self.s.unsign(bytesToken)
            driver = Driver.objects.get(pk=id)
            return driver
        except (ObjectDoesNotExist, BadSignature):
            raise BadTokenError()


class DriverAuthenticate(authentication.BaseAuthentication):

    def authenticateheader(self, request):
        username = request.META.get("X_DRIVER_TOKEN")
        if not username:
            return None
        try:
            return DriverAuth().verifytoken(username)
        except BadTokenError:
            raise exceptions.AuthenticationFailed("Bad Token Error")






#check header (driver token) X_DriverToken [/]
#verify token
#return driver object
#or driver none, failed exception