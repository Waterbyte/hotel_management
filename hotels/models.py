from django.core.exceptions import ValidationError
from django.db import models

from .utility import hotel_directory_path, room_directory_path


class HotelManager(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(blank=False)
    address = models.TextField(blank=False)
    city = models.TextField(blank=False)
    state = models.TextField(blank=False)
    country = models.TextField(blank=False)
    zip_code = models.TextField(blank=False)
    phone_number = models.TextField(blank=False)
    email_address = models.EmailField(blank=False)
    image = models.ImageField(blank=False, upload_to=hotel_directory_path)

    def clean(self):
        super().clean()
        model = self.__class__
        num_hotels = model.objects.count()
        if num_hotels >= 100:
            raise ValidationError("Max limit of 100 hotels reached.")

    def __str__(self):
        return str(self.id) + ": " + self.name


class RoomTypeManager(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(blank=False)
    price = models.IntegerField(blank=False)
    hotel_id_key = models.ForeignKey(HotelManager, on_delete=models.CASCADE)

    def clean(self):
        super().clean()
        model = self.__class__

        hotel_id = self.hotel_id_key
        num_room_type = model.objects.filter(hotel_id_key=hotel_id).count()
        if num_room_type >= 15:
            raise ValidationError("Max limit of 15 room type reached.")

        received_name = self.name
        name_present = model.objects.filter(hotel_id_key=hotel_id).filter(name=received_name)
        if name_present:
            raise ValidationError("Room of this type already present.")

    def __str__(self):
        return self.name


class RoomManager(models.Model):
    id = models.IntegerField(primary_key=True)
    room_name = models.TextField()
    room_type_key = models.ForeignKey(RoomTypeManager, on_delete=models.CASCADE)
    image = models.ImageField(blank=False, upload_to=room_directory_path)

    def clean(self):
        super().clean()
        model = self.__class__
        room_type_id = self.room_type_key

        num_room = model.objects.filter(room_type_key=room_type_id).count()
        if num_room >= 50:
            raise ValidationError("Max limit of 50 rooms reached for this room type.")

        received_room_name = self.room_name
        name_present = model.objects.filter(room_type_key=room_type_id).filter(room_name=received_room_name)
        if name_present:
            raise ValidationError("For current type, this room is already present")

    def __str__(self):
        return str(self.room_type_key) + "-" + self.room_name


class BookingManager(models.Model):
    id = models.IntegerField(primary_key=True)
    start_date = models.DateTimeField(blank=False)
    end_date = models.DateTimeField(blank=False)
    cust_full_name = models.TextField(blank=False, verbose_name='Customer Name')
    cust_mail_id = models.EmailField(blank=True, verbose_name='Customer Email')
    cust_phone_number = models.TextField(blank=False, verbose_name='Customer Phone')
    cust_pan_number = models.TextField(blank=True, verbose_name='Customer PAN')
    total_nights = models.IntegerField()
    total_price = models.IntegerField()
    receptionist_key = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    room_key = models.ForeignKey(RoomManager, on_delete=models.CASCADE, verbose_name='Room')
