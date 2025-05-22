from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model
User = get_user_model()

from .serializers import (
    DeviceSerializer,
    DeviceCreateSerializer,
    DeviceUpdateSerializer,
    ForeignDeviceSerializer,
    ForeignDeviceUpdateSerializer,
    LocationSerializer
)
from .models import Device, ForeignDevice

# device/<uuid:device_id>/location
class DeviceLocationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, device_id):
        try:
            device = Device.objects.get(id=device_id, owner=request.user)
        except Device.DoesNotExist:
            return Response({"error": "Device not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = LocationSerializer(device)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, device_id):
        try:
            device = Device.objects.get(id=device_id, owner=request.user)
        except Device.DoesNotExist:
            return Response({"error": "Device not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = LocationSerializer(device, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Device location updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# device/
class DeviceCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("Request data:", request.data)
        serializer = DeviceCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            device = serializer.save()
            print(DeviceSerializer(device).data)
            return Response({
                "message": "Device created successfully.",
                "device": DeviceSerializer(device).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# device/<uuid:device_id>/
class DeviceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, device_id):
        try:
            device = Device.objects.get(id=device_id, owner=request.user)
        except Device.DoesNotExist:
            return Response({"error": "Device not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = DeviceSerializer(device)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, device_id):
        try:
            device = Device.objects.get(id=device_id, owner=request.user)
        except Device.DoesNotExist:
            return Response({"error": "Device not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = DeviceUpdateSerializer(device, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Device updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# foreign_device/<uuid:device_id>/
class ForeignDeviceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, device_id):
        try:
            foreign_device = ForeignDevice.objects.get(id=device_id, user=request.user)
        except ForeignDevice.DoesNotExist:
            return Response({"error": "Foreign device not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ForeignDeviceSerializer(foreign_device)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, device_id):
        try:
            foreign_device = ForeignDevice.objects.get(id=device_id, user=request.user)
        except ForeignDevice.DoesNotExist:
            return Response({"error": "Foreign device not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ForeignDeviceUpdateSerializer(foreign_device, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Foreign device updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# device/<uuid:device_id>/share
class ShareDeviceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, device_id):
        target_username = request.data.get("username")

        if not target_username:
            return Response({"error": "Username is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            target_user = User.objects.get(username=target_username)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            device = Device.objects.get(id=device_id, owner=request.user)
        except Device.DoesNotExist:
            return Response({"error": "Device not found or not owned by you."}, status=status.HTTP_404_NOT_FOUND)

        if device.owner == target_user:
            return Response({"error": "You cannot share your own device as a foreign device."}, status=status.HTTP_400_BAD_REQUEST)

        if ForeignDevice.objects.filter(user=target_user, device=device).exists():
            return Response({"error": "Device is already shared with this user."}, status=status.HTTP_400_BAD_REQUEST)

        foreign_device = ForeignDevice.objects.create(
            user=target_user,
            device=device,
            alias=device.name
        )

        serializer = ForeignDeviceSerializer(foreign_device)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# device/<uuid:device_id>/delete
class DeleteDeviceView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, device_id):
        try:
            device = Device.objects.get(id=device_id, owner=request.user)
        except Device.DoesNotExist:
            return Response({"error": "Device not found or not owned by you."}, status=status.HTTP_404_NOT_FOUND)

        device.delete()

        return Response({"message": "Device deleted successfully."}, status=status.HTTP_200_OK)

# device/<uuid:device_id>/revoke
class RevokeForeignAccessView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, device_id):
        try:
            device = Device.objects.get(id=device_id, owner=request.user)
        except Device.DoesNotExist:
            return Response({"error": "Device not found or not owned by you."}, status=status.HTTP_404_NOT_FOUND)

        count, _ = ForeignDevice.objects.filter(device=device).delete()

        return Response(
            {"message": f"Access revoked. {count} foreign access removed."},
            status=status.HTTP_200_OK
        )
