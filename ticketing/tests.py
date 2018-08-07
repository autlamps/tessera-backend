import json
import rsa
import base64

from django.contrib.auth.models import User
from django.test import TestCase
from django.conf import settings
from rest_framework.test import APIRequestFactory, force_authenticate

from ticketing.api.userviews import NotificationView
from ticketing.models import Account, BalanceTicket
from ticketing.userticket.createqrcode import QRCode


class CreateNotificationTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user("fakeuser", "fakepassword")
        Account(user=self.user).save()
        self.acc = self.user.account.all()[0]
        self.factory = APIRequestFactory()
        self.view = NotificationView.as_view()

    def test_create_notification(self):
        req = self.factory.post('/api/v1/users/notifications/',
                                {"token": "1234"}, format='json')

        force_authenticate(req, user=self.user)

        resp = self.view(req).rendered_content
        resp_dict = json.loads(resp.decode('UTF-8'))

        self.assertEqual(resp_dict["success"], True)
        self.assertIsNotNone(resp_dict["created_id"])

        push = self.acc.notification_tokens.all()[0]

        self.assertIsNotNone(push)
        self.assertEqual(resp_dict['created_id'], push.id)


class SignTestCase(TestCase):

    def setUp(self):
        self.qrfactory = QRCode(testing=True)
        (pubKey, privKey) = rsa.newkeys(512)
        self.qrfactory.private = privKey
        self.qrfactory.public = pubKey

        self.user = User.objects.create_user("fakeuser", "fakepassword")
        Account(user=self.user).save()
        self.acc = self.user.account.all()[0]

        self.bt = BalanceTicket(account=self.acc, current_value=10,
                                qr_code_id="716190a3-849a-4d4a-a0a2-020cf40bda7d")
        self.bt.save()

    def testSigning(self):
        signed1 = self.qrfactory.createbtqrcode(self.bt)
        signed2 = self.qrfactory.createbtqrcode(self.bt)
        user1, hashed1 = signed1.split(":")
        user2, hashed2 = signed2.split(":")
        if user1 == user2:
            if hashed1 == hashed2:
                pass
            else:
                self.fail("The hashes are different")
        else:
            self.fail("The users are different")

    def testVerifying(self):
        signed = self.qrfactory.createbtqrcode(self.bt)
        ticket = self.qrfactory.verify(signed)
        qrcode = ticket['ticket'].qr_code_id
        type = ticket['type']
        if str(qrcode) != self.bt.qr_code_id:
            self.fail("The QR code is not the set one, got : "
                      + qrcode.__str__())
        if type != "b":
            self.fail("The type of ticket is not b, got : "
                      + type)

    def testPublicKey(self):
        testSignature = "This is a test"
        priv = settings.PRIVATE_KEY
        if priv == "":
            self.fail("There is no Private Key in the settings")
        header = priv[:32]
        body = priv[32:len(priv)-29].replace(" ", "\n")
        footer = priv[-29:]
        privkey = header + "\n" + body + footer
        private = rsa.PrivateKey.load_pkcs1(privkey)
        pub = settings.PUBLIC_KEY
        if pub == "":
            self.fail("There is no Public Key in the settings")
        header = pub[:31]
        body = pub[31:len(pub)-28].replace(" ", "\n")
        footer = pub[-28:]
        pubkey = header + "\n" + body + footer
        public = rsa.PublicKey.load_pkcs1(pubkey)
        signed = base64.b64encode(rsa.sign(testSignature.encode('UTF-8'),
                                           private, 'SHA-256'))
        if testSignature is signed:
            self.fail("The hashed message is incorrect, we got : "
                      "" + signed.__str__())
        else:
            hash = base64.b64decode(signed)
            try:
                rsa.verify(testSignature.encode(), hash, public)

            except rsa.VerificationError:
                self.fail("We are unable to verify the hashed message")
