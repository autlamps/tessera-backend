import json

from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from rest_framework.test import APIRequestFactory, force_authenticate

from ticketing.api.userviews import NotificationView
from ticketing.models import Account


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
