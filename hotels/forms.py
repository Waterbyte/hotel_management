from django.forms import ModelForm

from .models import HotelManager


class HotelEditForm(ModelForm):
    class Meta:
        model = HotelManager
        fields =['address','city','state','country','zip_code','phone_number','email_address','image']
