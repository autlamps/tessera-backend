from rest_framework import serializers

from ticketing.models import Announcement


class AnnouncementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Announcement
        fields = ('id', 'sent_at', 'title', 'short_description',
                  'long_description')