from datetime import datetime

import pytz
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from tessera import settings
from ticketing.driverauth.driverauthtoken import DriverAuth, DriverAuthenticate
from ticketing.models import Driver, Trip, BalanceTicketTrip, Route
from ticketing.api.driverserializers import DriverSerializer, \
    DriverAuthSerializer, CreateTripSerializer, InputTripSerializer
from ticketing.userticket.createqrcode import QRCode, VerifyFailedError


class DriverAuthTokenView(APIView):
    """
    DriverAuthTokenView returns a drivers auth token
    """

    def post(self, request, *args, **kwargs):
        divdata = DriverAuthSerializer(data=request.data)

        if not divdata.is_valid():
            return Response(data={"success": False})

        id = divdata.validated_data["id"]

        try:
            driver = Driver.objects.get(pk=id)
            auth = DriverAuth()
            token = auth.createtoken(id)

            return Response(data={"success": True, "token": token})
        except ObjectDoesNotExist:
            return Response(data={"success": False,
                                  "reason": "Driver not found"})

    def get(self, request, *args, **kwargs):
        drivers = Driver.objects.all()
        serializer = DriverSerializer(drivers, many=True)
        return Response(data=serializer.data)


class KeysView(APIView):
    """
    KeysView returns public keys for ticket authentications
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [DriverAuthenticate]

    def get(self, request, *args, **kwargs):
        return Response(data={
            "success": True,
            "public_key": settings.PUBLIC_KEY,
        })


class TripView(APIView):
    """
    TripView creates a new trip view and returns the created trip id
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [DriverAuthenticate]

    def post(self, request, *args, **kwargs):
        driver = request.user

        datain = InputTripSerializer(data=request.data)

        if not datain.is_valid():
            return Response(data={"success": False})

        route_id = datain.validated_data["route"]
        route = Route.objects.get(pk=route_id)

        try:
            trip = Trip(route=route,
                        driver=driver,
                        start=datetime.now(
                            tz=pytz.timezone('Pacific/Auckland')))
            trip.save()
            return JsonResponse(data={
                "success": True,
                "route": trip.route.id,
                "trip_id": trip.id
            })
        except ObjectDoesNotExist:
            return Response(data={"success": False,
                                  "reason": "Driver not found"})

    def delete(self, request, *args, **kwargs):
        # breaking rest semantics here but YOLO
        trip_id = self.kwargs.get("trip_id")

        trip = Trip.objects.get(pk=trip_id)
        trip.end = datetime.now(tz=pytz.timezone('Pacific/Auckland'))
        trip.save()

        return JsonResponse(data={"success": True})


class BTTripView(APIView):
    """
    BTTrip is called by the driver device to "tag" someone on

    THIS MUST BE IDEMPOTENT (it's not at this point :( )
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [DriverAuthenticate]

    def post(self, request, *args, **kwargs):
        data = CreateTripSerializer(data=request.data)
        qr = data.validated_data["qr_code"]
        trip_id = data.validated_data["trip_id"]

        try:
            trip = Trip.objects.get(pk=trip_id)
        except Trip.DoesNotExist:
            return Response(data={
                "success": False,
                "reason": "Trip doesn't exist"
            })

        try:
            verified = QRCode().verify(qr)
            ticket = verified["ticket"]

            # allow users to go negative but if they're already
            # negative no further
            if ticket.current_value > 0:
                prev_bal = ticket.current_value
                post_bal = ticket.current_value - trip.route.cost

                btt = BalanceTicketTrip(trip=trip,
                                        ticket=ticket,
                                        pre_bal=prev_bal,
                                        post_bal=post_bal)

                ticket.current_value = post_bal

                ticket.save()
                btt.save()

                return Response(data={
                    "success": True,
                    "user_current_bal": ticket.current_value
                })
            else:
                return Response(data={
                    "success": False,
                    "reason": "Insufficient funds."
                })
        except VerifyFailedError:
            return Response(data={
                "success": False,
                "reason": "QR Code Invalid"
            })

    def delete(self, request, *args, **kwargs):
        pass


class RTTripView(APIView):
    """
    RTTripView is called by driver to tag on a ticket

    THIS MUST BE IDEMPOTENT
    """

    def post(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass
