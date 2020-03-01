from django.urls import path

from .views import (IndexView, HotelProfile, HotelProfileEdit,
                    RoomTypeListView, RoomTypeAddView, RoomTypeDeleteView,
                    RoomListView, RoomAddView, RoomDeleteView)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('hotel/profile/', HotelProfile.as_view(), name='hotel_profile'),
    path('hotel/profile/edit', HotelProfileEdit.as_view(), name='hotel_profile_edit'),
    path('room-type/view', RoomTypeListView.as_view(), name='room_type_list'),
    path('room-type/add', RoomTypeAddView.as_view(), name='room_type_add'),
    path('room-type/delete/<int:pk>', RoomTypeDeleteView.as_view(), name='room_type_delete'),
    path('room/view', RoomListView.as_view(), name='room_list'),
    path('room/add', RoomAddView.as_view(), name='room_add'),
    path('room/delete/<int:pk>', RoomDeleteView.as_view(), name='room_delete')
]
