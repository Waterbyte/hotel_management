# Create your views here.
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, ListView, CreateView, DeleteView
from django.views.generic.base import TemplateView

from hotels.forms import HotelEditForm
from hotels.models import HotelManager, RoomTypeManager, RoomManager


# Generic class views for main page
# Functionality: Displaying
class IndexView(TemplateView):
    template_name = 'hotels/index.html'


# Generic class views for Hotel Profile
# Functionality: Listing, Updating
class HotelProfile(DetailView):
    model = HotelManager
    template_name = 'hotels/hotel_profile.html'

    def get_object(self):
        if self.request.user.is_authenticated and self.request.user.hotel:
            return get_object_or_404(HotelManager, pk=self.request.user.hotel.id)


class HotelProfileEdit(UpdateView):
    model = HotelProfile
    template_name = 'hotels/hotel_profile_edit.html'
    success_url = reverse_lazy('hotel_profile')
    form_class = HotelEditForm

    def get_object(self, queryset=None):
        if self.request.user.is_authenticated and self.request.user.hotel:
            return get_object_or_404(HotelManager, pk=self.request.user.hotel.id)


# Generic class views for Room Types
# Functionality: Listing, Creating and Deleting
class RoomTypeListView(ListView):
    template_name = 'hotels/room_types_list.html'
    model = RoomTypeManager

    def get_queryset(self):
        return super().get_queryset().filter(hotel_id_key=self.request.user.hotel.id)


class RoomTypeAddView(CreateView):
    model = RoomTypeManager
    template_name = 'hotels/room_types_add.html'
    fields = ['name', 'price', 'hotel_id_key']
    success_url = reverse_lazy('room_type_list')

    def get_initial(self):
        initial = super().get_initial()
        initial['hotel_id_key'] = self.request.user.hotel.id
        return initial

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.object.hotel_id_key.id == self.request.user.hotel.id:
            return super().form_valid(form)
        else:
            raise Http404


class RoomTypeDeleteView(DeleteView):
    model = RoomTypeManager
    success_url = reverse_lazy('room_type_list')

    def get(self, *args, **kwargs):
        if self.get_object().hotel_id_key.id == self.request.user.hotel.id:
            return self.delete(*args, **kwargs)
        else:
            raise Http404


# Generic class views for Rooms
# Functionality: Listing, Creating and Deleting
class RoomListView(ListView):
    template_name = 'hotels/room_list.html'
    model = RoomManager

    def get_queryset(self):
        room_types_inner = RoomTypeManager.objects.filter(hotel_id_key=self.request.user.hotel.id).values('id')
        return super().get_queryset().filter(room_type_key__in=room_types_inner)


class RoomAddView(CreateView):
    template_name = 'hotels/room_add.html'
    model = RoomManager
    fields = ['room_name', 'room_type_key', 'image']
    success_url = reverse_lazy('room_list')

    def get_initial(self):
        initial = super().get_initial()
        inner_qs = RoomTypeManager.objects.filter(hotel_id_key=self.request.user.hotel.id).values('id')
        initial['room_type_key'] = inner_qs
        return initial

    def form_valid(self, form):
        self.object = form.save(commit=False)
        room_types_inner = RoomTypeManager.objects.filter(hotel_id_key=self.request.user.hotel.id).values_list('id', flat=True)
        if self.object.room_type_key.id in room_types_inner:
            return super().form_valid(form)
        else:
            raise Http404


class RoomDeleteView(DeleteView):
    model = RoomManager
    success_url = reverse_lazy('room_list')

    def get(self, *args, **kwargs):
        room_types_inner = RoomTypeManager.objects.filter(hotel_id_key=self.request.user.hotel).values_list('id', flat=True)
        if self.get_object().room_type_key.id in room_types_inner:
            return self.delete(*args, **kwargs)
        else:
            raise Http404
