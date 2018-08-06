from django.http import HttpResponse
from django.http import JsonResponse
from ticketing.models import BalanceTicket

# Create your views here.
from ticketing.userticket.createqrcode import QRCode


def testsign(request):
    bt = BalanceTicket.objects.get(id=1)

    creator = QRCode()
    qr = creator.createbtqrcode(bt)
    print(qr)
    print(creator.verify(qr))
    return HttpResponse("yes")