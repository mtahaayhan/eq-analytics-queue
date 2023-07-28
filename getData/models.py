from django.db import models
import uuid

class File(models.Model):
    UUID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    file_name = models.CharField(max_length=100)
    file_type = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=50)

    def __str__(self):
        return self.file_name


class Earthquake(models.Model):
    UUID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    file_UUID = models.ForeignKey(File, on_delete=models.CASCADE)
    eq_datetime = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)
    latitude = models.CharField(max_length=255)
    depth = models.CharField(max_length=255)
    magnitude = models.CharField(max_length=255)

    def __str__(self):
        return f"Earthquake: {self.magnitude} ({self.eq_datetime})"
