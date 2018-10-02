from datetime import datetime

import pytz

from ticketing.models import Trip, Route


class TripCreator:
    """
    TripCreator, generates trips and also has functions to allow the trip to
    start or stop and then includes the current date time for it
    """
    def __init__(self, routename, driver):
        self.route = Route.objects.get(name=routename)
        self.driver = driver

    def starttrip(self):
        trip = Trip(route_id=self.route.id,
                    driver_id=self.driver.id,
                    start=datetime.now(tz=pytz.timezone('Pacific/Auckland')))
        trip.save()
        return trip

    def finishtrip(self, tripid):
        trip = Trip.objects.get(id=tripid)
        trip.objects.get().end = datetime.now(tz=pytz.timezone('Pacific/Auckland'))
        trip.save()
        return trip
