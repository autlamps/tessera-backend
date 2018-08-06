import base64
import rsa

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from ticketing.models import BalanceTicket, RideTicket

class VerifyFailedError(Exception):
    pass

class QRCode:
    """
    QRCode creator is used to create a user ticket/balance ID, which is then signed and then returned
    """

    # Refactor to QR Factory
    # Make QR codes for RT tickets

    def __init__(self, testing=False):
        if not testing:
            if settings.PRIVATE_KEY is None or settings.PUBLIC_KEY is None:
                raise Exception("The settings file has an issue with the keys")
            else:
                self.private = rsa.PrivateKey.load_pkcs1(self.__getprivkey())
                self.public = rsa.PublicKey.load_pkcs1(self.__getpubkey())

    @staticmethod
    def __getprivkey():
        priv = settings.PRIVATE_KEY
        header = priv[:32]
        body = priv[32:len(priv)-29].replace(" ", "\n")
        footer = priv[-29:]
        privkey = header + "\n" + body + footer
        return privkey

    @staticmethod
    def __getpubkey():
        pub = settings.PUBLIC_KEY
        header = pub[:31]
        body = pub[31:len(pub)-28].replace(" ", "\n")
        footer = pub[-28:]
        pubkey = header + "\n" + body + footer
        return pubkey

    def createbtqrcode(self, btticket: BalanceTicket):
        uid = btticket.qr_code_id
        type = 'b'
        val = 'x'
        name = btticket.account.user.first_name
        return self.__sign(uid, type, val, name)

    def creatertqrcode(self, rtticket: RideTicket):
        uid = rtticket.qr_code
        type = 'r'
        val = rtticket.initial_value
        name = rtticket.short_name
        return self.__sign(uid, type, val, name)

    def __sign(self, uid, type, val, name):
        tosign = str(uid) + '.' + type + '.' + val + '.' + name
        signed = base64.b64encode(rsa.sign(tosign.encode('UTF-8'), self.private, 'SHA-256'))
        toreturn = str(tosign) + ':' + str(signed.decode('UTF-8'))
        self.ID = toreturn
        return toreturn

    def verify(self, qrcode):
        parts = qrcode.split(':')
        hash = base64.b64decode(parts[1])
        try:
            rsa.verify(parts[0].encode(), hash, self.public)
            print("Verified")
            user = parts[0].split(".")
            uuid = user[0]
            ticketType = user[1]
            if ticketType == "b":
                try:
                    ticket = BalanceTicket.objects.get(qr_code=uuid)
                    return {"ticket": ticket, "type": ticketType}
                except ObjectDoesNotExist:
                    raise VerifyFailedError()
            elif ticketType == "r":
                try:
                    ticket = RideTicket.objects.get(qr_code=uuid)
                    return {"ticket": ticket, "type": ticketType}
                except ObjectDoesNotExist:
                    raise VerifyFailedError()
        except rsa.VerificationError:
            print("Verification Error")
            raise VerifyFailedError
            # Create an error for better usability
        print("Hash 0 : " + parts[0])
        print("Hash 1 : " + parts[1])
