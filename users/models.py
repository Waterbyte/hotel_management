# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

from hotels.models import HotelManager


class CustomUser(AbstractUser):
    hotel = models.ForeignKey(HotelManager, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.username
