from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token
from ticketing import views


from ticketing.api.bothviews import RouteView
from ticketing.api.userviews import TicketView, CardView, \
    TopUpView, UsersTripView, AnnouncementView, NotificationView

"""
usersapi.py sets up urls for the user api used by the passenger apps
"""

urlpatterns = [
    url(r'^authtokens/', obtain_auth_token, name='authtokenview'),
    url(r'^tickets/', TicketView.as_view(), name="ticketview"),
    url(r'^cards/', CardView.as_view(), name="cardview"),
    url(r'^topups/', TopUpView.as_view(), name="topupview"),
    url(r'^trips/', UsersTripView.as_view(), name='tripview'),
    url(r'^announcements/', AnnouncementView.as_view(),
        name='announcementview'),
    url(r'^notifications/', NotificationView.as_view(),
        name='notificationview'),
    url(r'^routes/', RouteView.as_view(), name='routeview')
]
