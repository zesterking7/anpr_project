from django.db import models

class LicensePlate(models.Model):
    number_plate = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='detected_plates/')
    toll_amount = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)  # New Column
