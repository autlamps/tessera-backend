from datetime import datetime

import pytz
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from tessera import settings
from ticketing.driverauth.driverauthtoken import DriverAuthenticate
from ticketing.api.driverserializers import DriverAuthSerializer, InputTripSerializer
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from ticketing.driverauth.driverauthtoken import DriverAuth
from ticketing.models import Driver, Trip
from ticketing.api.driverserializers import DriverSerializer, TripSerializer
from ticketing.trip.createtrip import TripCreator


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

        route = datain.validated_data["route"]

        try:
            tripC = TripCreator(route, driver)
            trip = tripC.starttrip()
            serializer = TripSerializer(trip)
            return JsonResponse(data=serializer.data)
        except ObjectDoesNotExist:
            return Response(data={"success": False,
                                  "reason": "Driver not found"})

    def delete(self, request, *args, **kwargs):
        trip_id = self.kwargs.get("trip_id")

        driver = request.user

        trip = Trip.objects.get(pk=trip_id)
        Trip.objects.get(pk=trip_id).end = datetime.now(tz=pytz.timezone('Pacific/Auckland'))
        serializer = TripSerializer(trip)

        return JsonResponse(data=serializer.data)


class BTTripView(APIView):
    """
    BTTrip is called by the driver device to "tag" someone on

    THIS MUST BE IDEMPOTENT
    """

    def post(self, request, *args, **kwargs):
        pass

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
