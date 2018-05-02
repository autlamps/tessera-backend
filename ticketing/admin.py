from django.contrib import admin

from ticketing.models import *

admin.site.register(Account)
admin.site.register(Announcement)
admin.site.register(Route)
admin.site.register(Driver)
admin.site.register(Trip)
admin.site.register(BalanceTicket)
admin.site.register(BalanceTicketTrip)
admin.site.register(Dispute)
admin.site.register(RideTicket)
admin.site.register(RideTicketTrip)
admin.site.register(TopUp)
admin.site.register(Card)
