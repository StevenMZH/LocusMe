from django.urls import path
from .views import (
    DeviceView,
    DeviceCreateView,
    ForeignDeviceView,

    DeviceLocationView,

    DeleteDeviceView,
    ShareDeviceView,
    RevokeForeignAccessView,
)

urlpatterns = [
    path('device/', DeviceCreateView.as_view()),
    path('device/<uuid:device_id>/', DeviceView.as_view()),
    path('foreign_device/<uuid:device_id>/', ForeignDeviceView.as_view()),

    path('device/<uuid:device_id>/location/', DeviceLocationView.as_view()),

    path('device/<uuid:device_id>/delete/', DeleteDeviceView.as_view()),
    path('device/<uuid:device_id>/share/', ShareDeviceView.as_view()),
    path('device/<uuid:device_id>/revoke/', RevokeForeignAccessView.as_view()),
]
