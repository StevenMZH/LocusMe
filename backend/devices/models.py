from django.db import models
import uuid

class Device(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='devices')
    
    name = models.CharField(max_length=30, blank=True)
    location = models.JSONField(default=list, blank=True)    # Placeholder type
    upload_frequency = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.name} - {self.owner.username}'s Device"
    

class ForeignDevice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    alias = models.CharField(max_length=30, blank=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='foreign_devices')
    device = models.ForeignKey('Device', on_delete=models.CASCADE, related_name='foreign_links')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'device')

    def __str__(self):
        return f"{self.alias or 'No alias'} - {self.user.username}'s Foreign Device"

