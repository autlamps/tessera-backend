from rest_framework import serializers


class DriverPinSerializer(serializers.Serializer):
    pin = serializers.IntegerField(read_only=True)


class DriverAuthSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    pin = serializers.IntegerField(required=True)


class DriverSerializer(serializers.Serializer):
    name = serializers.CharField()
    id = serializers.IntegerField()
