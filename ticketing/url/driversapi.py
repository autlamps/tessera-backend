from django.conf.urls import url

from ticketing.api.bothviews import PingView, RouteView
from ticketing.api.driverviews import DriverAuthTokenView, KeysView, \
    BTTripView, RTTripView, TripView

"""
driversapi.py sets up urls for the user api used by the passenger apps
"""

urlpatterns = [
    url(r'^authtokens/', DriverAuthTokenView.as_view(),
        name="driverauthtokenview"),
    url(r'^ping/', PingView.as_view(), name='pingview'),
    url(r'^keys/', KeysView.as_view(), name='keysview'),
    url(r'^routes/', RouteView.as_view(), name='routeview'),
    url(r'^trips/', TripView.as_view(), name='tripview'),
    url(r'^bttrips/', BTTripView.as_view(), name='bttripview'),
    url(r'^rttrips/', RTTripView.as_view(), name='rttripview')
]
