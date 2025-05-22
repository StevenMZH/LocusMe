from rest_framework import serializers
from .models import Device, ForeignDevice

class DeviceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'name', 'upload_frequency', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'owner', 'name', 'location', 'upload_frequency', 'updated_at']
        read_only_fields = ['id', 'updated_at']

class DeviceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['name', 'upload_frequency']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['location']



class ForeignDeviceSerializer(serializers.ModelSerializer):
    device = serializers.PrimaryKeyRelatedField(
        queryset=Device.objects.all(),  
        write_only=True
    )
    
    class Meta:
        model = ForeignDevice
        fields = ['id', 'alias', 'user', 'device', 'updated_at']
        read_only_fields = ['id', 'updated_at']

    def validate(self, attrs):
        user = attrs.get('user')
        device = attrs.get('device')

        if device.owner == user:
            raise serializers.ValidationError("You cannot register your own device as a foreign device.")

        if ForeignDevice.objects.filter(user=user, device=device).exists():
            raise serializers.ValidationError("This device is already registered as a foreign device for this user.")

        return attrs

class ForeignDeviceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForeignDevice
        fields = ['alias']


