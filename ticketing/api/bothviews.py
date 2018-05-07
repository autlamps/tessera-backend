"""
bothviews.py contains views that both drivers and users use
"""
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.views import APIView


class PingView(APIView):
    """
    PingView returns true on a get request
    """

    def get(self, request, *args, **kwargs):
        pong = dict()
        pong['pong'] = True

        return Response(pong, status=200)


class RouteView(mixins.ListModelMixin, generics.GenericAPIView):
    """
    RouteView returns all routes
    """

    # TODO: setup queryset and serializer

    def list(self, request, *args, **kwargs):
        pass
