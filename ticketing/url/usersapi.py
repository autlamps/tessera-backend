from django.conf.urls import url

from ticketing.api.userviews import AuthTokenView, TicketView, CardView, \
    TopUpView, TripView, AnnouncementView, NotificationView

"""
usersapi.py sets up urls for the user api used by the passenger apps
"""

urlpatterns = [
    url(r'^authtokens/', AuthTokenView.as_view(), name='authtokenview'),
    url(r'^tickets/', TicketView.as_view(), name="ticketview"),
    url(r'^cards/', CardView.as_view(), name="cardview"),
    url(r'^topups/', TopUpView.as_view(), name="topupview"),
    url(r'^trips/', TripView.as_view(), name='tripview'),
    url(r'^announcements/', AnnouncementView.as_view(),
        name='announcementview'),
    url(r'^notifications/', NotificationView.as_view(),
        name='notificationview')
]
