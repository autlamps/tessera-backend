from django.db import models
import django.contrib.auth


class Account(models.Model):
    # abstraction over User so we can allow multiple sign in methods
    user = models.ForeignKey(django.contrib.auth.get_user_model(),
                             on_delete=models.CASCADE, related_name='account')

    def __str__(self):
        return self.user.username


class PushNotification(models.Model):
    account = models.ForeignKey('Account', on_delete=models.CASCADE,
                                related_name='notification_tokens')
    token = models.CharField(max_length=162)
    expire = models.BooleanField(default=False)


class Announcement(models.Model):
    sent_at = models.DateTimeField()
    title = models.CharField(max_length=25)
    short_description = models.CharField(max_length=50)
    long_description = models.CharField(max_length=1000)

    def __str__(self):
        return self.title


class Route(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=90)
    cost = models.FloatField(max_length=500)

    def __str__(self):
        return self.name


class Driver(models.Model):
    name = models.CharField(max_length=50)
    pin = models.IntegerField()

    def __str__(self):
        return self.name

    def is_authenticated(self):
        return True


class Trip(models.Model):
    route = models.ForeignKey('Route', on_delete=models.PROTECT)
    driver = models.ForeignKey('Driver', on_delete=models.PROTECT)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True)

    def __str__(self):
        return self.route.name + "-" + self.driver.name


class BalanceTicket(models.Model):
    account = models.ForeignKey('Account',  related_name='balance_ticket',
                                on_delete=models.CASCADE)
    current_value = models.FloatField()
    qr_code_id = models.UUIDField()

    def __str__(self):
        return self.account.user.username + " - " + str(self.current_value)


class BalanceTicketTrip(models.Model):
    trip = models.ForeignKey('Trip', on_delete=models.PROTECT)
    ticket = models.ForeignKey('BalanceTicket', on_delete=models.PROTECT)
    pre_bal = models.FloatField()
    post_bal = models.FloatField()

    def __str__(self):
        return self.ticket.account.user.username + " - " + self.trip.__str__()


class Dispute(models.Model):
    active = models.BooleanField()
    bt_trip = models.ForeignKey('BalanceTicketTrip', on_delete=models.PROTECT)
    account = models.ForeignKey('Account', on_delete=models.PROTECT)
    title = models.CharField(max_length=100)
    message = models.CharField(max_length=400)

    def __str__(self):
        return self.account.user.username + ": " + self.id


class RideTicket(models.Model):
    current_rides = models.IntegerField()
    initial_value = models.IntegerField()
    qr_code = models.UUIDField()
    created_at = models.DateTimeField()
    valid_for = models.ManyToManyField('Route')
    short_name = models.CharField(max_length=10)


class RideTicketTrip(models.Model):
    trip = models.ForeignKey('Trip', on_delete=models.PROTECT)
    rt = models.ForeignKey('RideTicket', on_delete=models.PROTECT)
    pre_bal = models.IntegerField()
    post_bal = models.IntegerField()


class TopUp(models.Model):
    balance = models.ForeignKey('BalanceTicket', on_delete=models.PROTECT)
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    pre_bal = models.FloatField()
    post_bal = models.FloatField()
    amount = models.FloatField()
    card = models.ForeignKey('Card', on_delete=models.PROTECT)

    def __str__(self):
        return self.account.user.username + ": " + self.amount


class Card(models.Model):
    # the credit card value is not stored only the token which is the value
    # returned by the payment processor to represent a card. We use expiry
    # date to remind users to update their card
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    description = models.CharField(max_length=10)
    token = models.CharField(max_length=100)
    expiry = models.DateField()
    name = models.CharField(max_length=10)
