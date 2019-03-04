from app import models
from rest_framework import serializers


class RoleSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()


class DeviceSerializer(serializers.Serializer):
    
    id = serializers.IntegerField()
    type = serializers.CharField()
    os = serializers.CharField()
    model = serializers.CharField()
    icon = serializers.CharField()

    class Meta:
        model = models.Device
        fields = ('id')


class UserSerializer(serializers.ModelSerializer):

    role = RoleSerializer()

    class Meta:
        model = models.User
        fields = ('id', 'fullname', 'username', 'email', 'avatar', 'role')


class AccesstorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Accessory
        fields = ('id', 'name', 'action', 'pin_id', 'created_at', 'updated_at')


class LogSerializer(serializers.ModelSerializer):

    user = UserSerializer()
    device = DeviceSerializer()
    accessory = AccesstorySerializer()
    
    class Meta:
        model = models.Log
        fields = ('id', 'user', 'device', 'accessory', 'checked', 'created_at')
