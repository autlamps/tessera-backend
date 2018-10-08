from django.urls import path

from ticketing.api.bothviews import PingView, RouteView
from ticketing.api.driverviews import DriverAuthTokenView, KeysView, \
    BTTripView, RTTripView, TripView

"""
driversapi.py sets up urls for the user api used by the passenger apps
"""

urlpatterns = [
    path('authtokens/', DriverAuthTokenView.as_view(),
         name="driverauthtokenview"),
    path('ping/', PingView.as_view(), name='pingview'),
    path('keys/', KeysView.as_view(), name='keysview'),
    path('routes/', RouteView.as_view(), name='routeview'),
    path('trips/', TripView.as_view(), name='tripview'),
    path('trips/<int:trip_id>/', TripView.as_view(), name='tripview'),
    path('bttrips/', BTTripView.as_view(), name='bttripview'),
    path('rttrips/', RTTripView.as_view(), name='rttripview')
]
