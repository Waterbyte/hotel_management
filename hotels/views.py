# Create your views here.
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, ListView, CreateView, DeleteView
from django.views.generic.base import TemplateView

from hotels.forms import HotelEditForm
from hotels.models import HotelManager, RoomTypeManager


class IndexView(TemplateView):
    template_name = 'hotels/index.html'


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


class RoomTypeListView(ListView):
    template_name = 'hotels/room_types.html'
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

    def get_queryset(self):
        return super().get_queryset().filter(hotel_id_key=self.request.user.hotel.id)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.object.hotel_id_key == self.request.user.hotel.id:
            self.object.save()
        return super().form_valid(form)


class RoomTypeDeleteView(DeleteView):
    model = RoomTypeManager
    success_url = reverse_lazy('room_type_list')

    def get(self, *args, **kwargs):
        if self.get_object().hotel_id_key == self.request.user.hotel:
            return self.delete(*args, **kwargs)
        else:
            raise Http404
