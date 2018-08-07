from rest_framework import serializers


class DriverPinSerializer(serializers.Serializer):
    pin = serializers.IntegerField(read_only=True)
