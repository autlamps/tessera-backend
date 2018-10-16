import pytz

from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from ticketing.models import Driver, Route, Trip
from ticketing.driverauth.driverauthtoken import DriverAuth


class TripTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="bobbytables",
                                             password="fakepassword")

        self.driver = Driver(name="Bobby Tables", pin=1234)
        self.driver.save()
        auth = DriverAuth()
        self.token = auth.createtoken(id=self.driver.id)

        self.route = Route(name="Fairy Lane",
                           description="This is a test", cost=1)
        self.route.save()
        self.trip = Trip(route=self.route, driver=self.driver,
                         start=datetime.now(
                             tz=pytz.timezone('Pacific/Auckland')))
        self.trip.save()

        self.client = APIClient()
        self.client.credentials(HTTP_X_DRIVER_TOKEN=self.token)

    def test_CreateTrip(self):
        response = self.client.post('/api/v1/drivers/trips/',
                                    {'route': self.route.id},
                                    format='json')

        if response.status_code != 200:
            self.fail("Was unable to create a trip, got status code " +
                      str(response.status_code))

    def test_StopTrip(self):
        response = self.client.delete('/api/v1/drivers/trips' +
                                      '/{}/'.format(self.trip.id))

        if response.status_code != 200:
            self.fail("Was unable to stop a trip, got status code "
                      + str(response.status_code))

        self.trip.refresh_from_db()

        if self.trip.end is None:
            self.fail("The end time of the trip was not found")
