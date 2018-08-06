from django.conf.urls import url

from ticketing.views import testsign

urlpatterns = [
    url(r'^runsign/', testsign, name="driverauthtokenview"),
]
