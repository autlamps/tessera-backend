import time
import datetime
import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework import mixins, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from ticketing.api.userserializers import AnnouncementSerializer, \
    NotificationTokenSerializer, SuccessSerializer, TripSerializer, \
    TicketSerializer
from ticketing.models import Announcement, PushNotification, Account, \
    BalanceTicketTrip, BalanceTicket


class TicketView(APIView):
    """
    TicketView returns a user's current BalanceTicket and allows them to
    request a new qr code via the PATCH method
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        try:
            bt = request.user.account.all()[0].balance_ticket.all()[0]
            serializer = TicketSerializer(bt)
            return JsonResponse(data=serializer.data)
        except ObjectDoesNotExist:
            qr = uuid.uuid4
            BalanceTicket(account=request.user.account.all()[0],
                          current_value=0, qrcode=qr)
            return JsonResponse(data={"error": "true"}, status=400)

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


class UsersTripView(generics.GenericAPIView, mixins.ListModelMixin):
    """
    TripView allows us to get all BalanceTicketTrips the user has taken
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TripSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        balance_ticket = \
            self.request.user.account.all()[0].balance_ticket.all()[0]
        return BalanceTicketTrip.objects.filter(ticket_id=balance_ticket.id)


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


class NotificationView(generics.GenericAPIView):
    """
    NotificationView registers a users push notification token
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = NotificationTokenSerializer

    def post(self, request, *args, **kwargs):
        tkdata = NotificationTokenSerializer(data=request.data)

        if not tkdata.is_valid():
            return Response(data={"success": False})

        token = tkdata.validated_data["token"]

        p = PushNotification(account=request.user.account.all()[0],
                             token=token)
        p.save()

        return Response(data={"success": True, "created_id": p.id})
