from django.urls import path

from .views import IndexView, HotelProfile, HotelProfileEdit

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('hotel/profile/', HotelProfile.as_view(), name='hotel_profile'),
    path('hotel/profile/edit', HotelProfileEdit.as_view(), name='hotel_profile_edit'),
]
