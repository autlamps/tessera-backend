import json
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from ticketing.api.userviews import NotificationView
from ticketing.models import Account, Driver
from ticketing.driverauth.driverauthtoken import DriverAuth, BadTokenError

class DriverIdTestCase(TestCase):

    def setUp(self):
        self.driver = Driver(name="Bobby Tables", pin=1234)
        self.driver.save()

    def test_create_token(self):
        auth = DriverAuth()
        token = auth.createtoken(self.driver.id)
        if token != "MS43cjJGQXB4SjZOcmZsb01fQjUteWY0MC1PeEU=":
            self.fail("Token doesn't match expected. Got " + token +
                      " expected MS43cjJGQXB4SjZOcmZsb01fQjUteWY0MC1PeEU=")

    def test_verify_token_pass(self):
        auth = DriverAuth()
        try:
            verify = auth.verifytoken("MS43cjJGQXB4SjZOcmZsb01fQjUt"
                                      "eWY0MC1PeEU=")
            if verify.id != self.driver.id:
                self.fail("Driver id is different expected: " + verify.id +
                          " got: " + self.driver.id)
        except BadTokenError:
            self.fail("Object does no exist")

    def test_very_token_fail(self):
        auth = DriverAuth()
        try:
            verify = auth.verifytoken("MS43cjJGQXB4SjZOcmZsb01fQjUte"
                                      "WY0MC1PeXX=")

            if verify.id is self.driver.id:
                pass
            # should only reach here if verify function is incorrect
            self.fail("Token doesn't match expected. Got " + auth.__str__() +
                      " expected incorrect token")
        except BadTokenError:
            print()
            self.fail("Object does not exist")


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