import datetime

from rest_framework import mixins, generics
from rest_framework.views import APIView

from ticketing.api.userserializers import AnnouncementSerializer
from ticketing.models import Announcement


class AuthTokenView(APIView):
    """
    AuthTokenView allows a user to login and is given a auth token in reponse
    """

    def post(self, request, *args, **kwargs):
        pass


class TicketView(APIView):
    """
    TicketView returns a user's current BalanceTicket and allows them to
    request a new qr code via the PATCH method
    """

    def get(self, request, *args, **kwargs):
        pass

    def patch(self, request, *args, **kwargs):
        pass


class CardView(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               mixins.RetrieveModelMixin,
               mixins.DestroyModelMixin,
               generics.GenericAPIView):
    """
    ClassView allows users to update and delete cards
    """

    # TODO: make sure we setup proper queryset so we don't get ALL credit cards
    # only cards the user owns...

    def list(self, request, *args, **kwargs):
        pass

    def create(self, request, *args, **kwargs):
        pass

    def retrieve(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass


class TopUpView(APIView):
    """
    TopUpView allows us to execute a new topup and list topups
    """

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass


class TripView(mixins.ListModelMixin,
               generics.GenericAPIView):
    """
    TripView allows us to get all trips
    """

    def list(self, request, *args, **kwargs):
        pass


class AnnouncementView(mixins.ListModelMixin,
                       generics.GenericAPIView):
    """
    AnnouncementView returns announcements from the last 30 days
    """

    queryset = Announcement.objects.filter(sent_at__gte=(
            datetime.datetime.now() + datetime.timedelta(-30)))

    serializer_class = AnnouncementSerializer

    def list(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class NotificationView(mixins.CreateModelMixin,
                       generics.GenericAPIView):
    """
    NotificationView registers a users push notification token
    """

    def create(self, request, *args, **kwargs):
        pass