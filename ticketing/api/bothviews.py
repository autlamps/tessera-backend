"""
bothviews.py contains views that both drivers and users use
"""
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.views import APIView

from ticketing.api.bothserializers import RouteSerializer
from ticketing.models import Route


class PingView(APIView):
    """
    PingView returns true on a get request
    """

    def get(self, request, *args, **kwargs):
        pong = dict()
        pong['pong'] = True

        return Response(pong, status=200)


class RouteView(generics.ListAPIView):
    """
    RouteView returns all routes
    """
    serializer_class = RouteSerializer
    queryset = Route.objects.all()
