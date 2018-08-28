from unittest import TestCase

from ticketing.driverauth.driverauthtoken import DriverAuth, BadTokenError
from ticketing.models import Driver


class DriverIdTestCase(TestCase):

    def setUp(self):
        self.driver = Driver(name="Bobby Tables", pin=1234)
        self.driver.save()

    def test_create_token(self):
        auth = DriverAuth(secret_key="thisisatest")
        token = auth.createtoken(self.driver.id)
        if token != "MS45LU03aF9sUVVDVEZYVDRDOGZ5WFF0TlhYMVk=":
            self.fail("Token doesn't match expected. Got " + token +
                      " expected MS45LU03aF9sUVVDVEZYVDRDOGZ5WFF0TlhYMVk=")

    def test_verify_token_pass(self):
        auth = DriverAuth(secret_key="thisisatest")
        try:
            verify = auth.verifytoken("MS45LU03aF9sUVVDVEZYV"
                                      "DRDOGZ5WFF0TlhYMVk=")
            if verify.id != self.driver.id:
                self.fail("Driver id is different expected: " + verify.id +
                          " got: " + self.driver.id)
            else:
                pass
        except BadTokenError:
            self.fail("Object does not exist")

    def test_very_token_fail(self):
        auth = DriverAuth(secret_key="thisisiatest")
        try:
            verify = auth.verifytoken("MS43cjJGQXB4SjZOcmZsb01fQj"
                                      "UteWY0MC1PeXX=")

            if verify.id is self.driver.id:
                pass
            # should only reach here if verify function is incorrect
            self.fail("Exec continued")
        except BadTokenError:
            pass
