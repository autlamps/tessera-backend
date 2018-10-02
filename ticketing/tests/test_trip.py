import pytz

from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase, Client
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

        self.client = Client()
        self.client.login(username="bobbytables", password="fakepassword")

    def test_CreateTrip(self):
        print(self.token)
        response = self.client.post('/api/v1/drivers/trips/', json={'route': 0},
                                    headers={'HTTP_X_DRIVER_TOKEN': self.token})

        if response.status_code != 200:
            self.fail("Was unable to create a trip, got status code "+
                      str(response.status_code))

    def test_StopTrip(self):
        response = self.client.delete('api/v1/drivers/trips/'+str(self.trip.id),
                                      headers={'HTTP_X_DRIVER_TOKEN':
                                      self.token})

        if response.status_code != 200:
             self.fail("Was unable to stop a trip, got status code "
                              + str(response.status_code))

        if self.trip.end is None:
            self.fail("The end time of the trip was not found")
