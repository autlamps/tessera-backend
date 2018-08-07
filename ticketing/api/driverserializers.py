from rest_framework import serializers


class DriverAuthSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    pin = serializers.IntegerField(required=True)


class DriverSerializer(serializers.Serializer):
    name = serializers.CharField()
    id = serializers.IntegerField()
