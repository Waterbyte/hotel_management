# Create your views here.
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, ListView, CreateView, DeleteView
from django.views.generic.base import TemplateView

from hotels import utility
from hotels.models import HotelManager, RoomTypeManager, RoomManager, BookingManager


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
    model = HotelManager
    template_name = 'hotels/hotel_profile_edit.html'
    success_url = reverse_lazy('hotel_profile')
    fields = ['address', 'city', 'state', 'country', 'zip_code', 'phone_number', 'email_address', 'image']

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

    def get_form(self, form_class=None):
        form = super(CreateView, self).get_form(form_class)
        form.fields['room_type_key'].queryset = RoomTypeManager.objects.filter(hotel_id_key=self.request.user.hotel.id)
        return form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        room_types_inner = RoomTypeManager.objects.filter(hotel_id_key=self.request.user.hotel.id).values_list('id',
                                                                                                               flat=True)
        if self.object.room_type_key.id in room_types_inner:
            return super().form_valid(form)
        else:
            raise Http404


class RoomDeleteView(DeleteView):
    model = RoomManager
    success_url = reverse_lazy('room_list')

    def get(self, *args, **kwargs):
        room_types_inner = RoomTypeManager.objects.filter(hotel_id_key=self.request.user.hotel).values_list('id',
                                                                                                            flat=True)
        if self.get_object().room_type_key.id in room_types_inner:
            return self.delete(*args, **kwargs)
        else:
            raise Http404


# Generic class views for Booking
# Functionality: Listing, Creating and Deleting
class BookingListView(ListView):
    template_name = 'hotels/booking_list.html'
    model = BookingManager

    def get_queryset(self):
        return super().get_queryset().filter(receptionist_key=self.request.user)


class BookingAddView(CreateView):
    template_name = 'hotels/booking_add.html'
    model = BookingManager
    fields = ['start_date', 'end_date', 'cust_full_name', 'cust_mail_id', 'cust_phone_number',
              'cust_pan_number', 'room_key']
    success_url = reverse_lazy('booking_list')

    def get_available_rooms(self):
        booked_room = BookingManager.objects.filter(receptionist_key=self.request.user)
        rooms = RoomManager.objects.filter(room_type_key__hotel_id_key=self.request.user.hotel.id).exclude(
            id__in=[o.room_key.id for o in booked_room])
        return rooms

    def get_form(self, form_class=None):
        form = super(CreateView, self).get_form(form_class)
        form.fields['room_key'].queryset = self.get_available_rooms()
        return form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        all_room = RoomManager.objects.filter(room_type_key__hotel_id_key=self.request.user.hotel.id) \
            .values_list('id', flat=True)
        if self.object.room_key.id in all_room:
            room_chosen = self.object.room_key.id
            room_type_chosen = RoomManager.objects.get(id=room_chosen).room_type_key.id
            room_type_price = RoomTypeManager.objects.get(id=room_type_chosen).price

            self.object.total_nights = utility.calculate_nights(self.object)
            self.object.total_price = room_type_price * self.object.total_nights
            self.object.receptionist_key = self.request.user
            return super(BookingAddView, self).form_valid(form)
        else:
            raise Http404


class BookingDeleteView(DeleteView):
    model = BookingManager
    success_url = reverse_lazy('booking_list')

    def get(self, *args, **kwargs):
        if self.get_object().receptionist_key.id == self.request.user.id:
            return self.delete(*args, **kwargs)
        else:
            raise Http404


class BookingEditView(UpdateView):
    model = BookingManager
    template_name = 'hotels/booking_edit.html'
    success_url = reverse_lazy('booking_list')
    fields = ['start_date', 'end_date', 'cust_full_name', 'cust_mail_id', 'cust_phone_number',
              'cust_pan_number', 'room_key']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # update only for change in start_date and end_date

        if 'start_date' in form.changed_data or 'end_date' in form.changed_data:
            all_room = RoomManager.objects.filter(room_type_key__hotel_id_key=self.request.user.hotel.id) \
                .values_list('id', flat=True)
            if self.object.room_key.id in all_room:
                room_chosen = self.object.room_key.id
                room_type_chosen = RoomManager.objects.get(id=room_chosen).room_type_key.id
                room_type_price = RoomTypeManager.objects.get(id=room_type_chosen).price

                self.object.total_nights = utility.calculate_nights(self.object)
                self.object.total_price = room_type_price * self.object.total_nights
                return super(BookingEditView, self).form_valid(form)
            else:
                raise Http404
        else:
            return super(BookingEditView, self).form_valid(form)
