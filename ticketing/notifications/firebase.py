import json

import firebase_admin
from firebase_admin import credentials

from django.conf import settings
from firebase_admin.messaging import Message, Notification, ApiCallError

from ticketing.models import Announcement


class Notifications:

    def __init__(self, dry_run=False):
        self.dry_run = dry_run
        cred_json = json.loads(settings.FIREBASE_KEY)
        self.cred = credentials.Certificate(cred_json)
        self.default_app = firebase_admin.initialize_app(self.cred)

    def broadcast(self, announcement: Announcement):
        msg = Message(
            notification=Notification(
                title=announcement.title,
                body=announcement.long_description,
            ),
            topic="/all/",
        )

        try:
            firebase_admin.messaging.send(msg, dry_run=self.dry_run)
            return True, None
        except (ApiCallError, ValueError) as e:
            return False, e.message

    def send_individual(self, title, message, token):
        pass
