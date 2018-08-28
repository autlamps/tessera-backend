import datetime

from ticketing.models import Driver, Trip, Route


class TripCreator:
    """
    TripCreator, generates trips and also has functions to allow the trip to
    start or stop and then includes the current date time for it
    """
    def __init__(self, routename, driverid):
        self.route = Route.objects.get(name=routename)
        self.driver = Driver.objects.get(id=driverid)

    def starttrip(self):
        trip = Trip(self.route, self.driver,
                    datetime.datetime(2012, 4, 1, 0, 0).timestamp(), 0)
        trip.save()
        return self

    def finishtrip(self, tripid):
        trip = Trip.objects.get(id=tripid)
        trip.objects.get().update(end=datetime.datetime(2012, 4, 1, 0, 0).timestamp())
        trip.save()
