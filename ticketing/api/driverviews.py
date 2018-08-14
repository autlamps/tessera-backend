from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.views import APIView
from ticketing.driverauth.driverauthtoken import DriverAuth
from ticketing.models import Driver
from ticketing.api.driverserializers import DriverSerializer


class DriverAuthTokenView(APIView):
    """
    DriverAuthTokenView returns a drivers auth token
    """

    def post(self, request, *args, **kwargs):
        divdata = DriverAuthTokenView(data=request.data)

        if not divdata.is_valid():
            return Response(data={"success": False})

        id = divdata.validated_data["id"]

        try:
            driver = Driver.objects.get(pk=id)
            auth = DriverAuth()
            token = auth.createtoken(id)

            return Response(data={"success": True, "token": token})
        except ObjectDoesNotExist:
            return Response(data={"success": False, "reason": "Driver not found"})

    def get(self, request, *args, **kwargs):
        drivers = Driver.objects.all()
        serializer = DriverSerializer(drivers, many=True)
        return Response(data=serializer.data)


class KeysView(APIView):
    """
    KeysView returns public keys for ticket authentications
    """

    def get(self, request, *args, **kwargs):
        pass


class TripView(APIView):
    """
    TripView creates a new trip view and returns the created trip id
    """

    def post(self, request, *args, **kwargs):
        pass


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
