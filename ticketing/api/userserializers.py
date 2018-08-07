import time
from rest_framework import serializers

from ticketing.userticket.createqrcode import QRCode
from ticketing.models import Announcement, BalanceTicketTrip, BalanceTicket


class AnnouncementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Announcement
        fields = ('id', 'sent_at', 'title', 'short_description',
                  'long_description')


class NotificationTokenSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)


class SuccessSerializer(serializers.Serializer):
    success = serializers.BooleanField
    created_id = serializers.CharField


class TicketSerializer(serializers.ModelSerializer):
    ttl = serializers.SerializerMethodField()
    qr_code = serializers.SerializerMethodField()

    class Meta:
        model = BalanceTicket
        fields = ['current_value', 'qr_code', 'ttl']

    def get_ttl(self, obj):
        return int(time.time()) + 43200

    def get_qr_code(self, obj):
        return QRCode().createbtqrcode(btticket=obj)

class TripSerializer(serializers.ModelSerializer):
    trip_name = serializers.SerializerMethodField()
    trip_start = serializers.SerializerMethodField()

    class Meta:
        model = BalanceTicketTrip
        fields = ('trip_name', 'trip_start', 'pre_bal', 'post_bal', 'id')

    def get_trip_name(self, obj):
        return obj.trip.route.name

    def get_trip_start(self, obj):
        return obj.trip.start.timestamp()
