import pytz

from datetime import datetime
from django.test import TestCase, Client
from ticketing.models import Driver, Route, Trip


class TripTest(TestCase):

    def setUp(self):
        self.driver = Driver(name="bobbytables", pin=1234)
        self.driver.save()

        self.route = Route(name="Fairy Lane",
                           description="This is a test", cost=1)
        self.route.save()

        self.client = Client()
        self.client.login(username="bobbytables", password="1234")

    def test_CreateTrip(self):
        response = self.client.post('/api/v1/drivers/trips/', {'route': 1})

        if response.status_code != 200:
            self.fail("Was unable to create a trip, got status code "+
                      response.status_code)

        self.trip = Trip(route=self.route, driver=self.driver,
                         start=datetime.now(
                             tz=pytz.timezone('Pacific/Auckland')))
        self.trip.save()

    def test_StopTrip(self):
        response = self.client.delete('api/v1/drivers/trips/'+self.trip.id)

        if response.status_code != 200:
             self.fail("Was unable to stop a trip, got status code "
                              + response.status_code)

        if self.trip.end is None:
            self.fail("The end time of the trip was not found")
