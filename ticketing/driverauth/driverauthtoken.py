import base64

from itsdangerous import Signer

from tessera import settings

from ticketing.models import Driver
from itsdangerous import BadSignature
from django.core.exceptions import ObjectDoesNotExist


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


#get token [x]
#check the token against existing tokens
#return driver object
#else throw error