from django.db import models

class LicensePlate(models.Model):
    number_plate = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='detected_plates/')
