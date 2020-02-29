# Create your views here.
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView
from django.views.generic.base import TemplateView

from hotels.forms import HotelEditForm
from hotels.models import HotelManager


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

