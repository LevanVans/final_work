from datetime import datetime
import decimal
from django.shortcuts import render, get_object_or_404, redirect
from .models import Hotel, Room, Booking
from django.db.models import Q
from .serializers import HotelSerializer, RoomSerializer, BookingSerializer
from rest_framework import viewsets



def home(request):
    available_rooms = Room.objects.filter(available=True)[:5]
    return render(request, 'home.html', {'available_rooms': available_rooms})

def hotel_list(request):
    hotels = Hotel.objects.all()
    city = request.GET.get('city')
    if city:
        hotels = hotels.filter(city__icontains=city)
    return render(request, 'hotel_list.html', {'hotels': hotels})

def room_list(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    rooms = hotel.room_set.all()
    room_type = request.GET.get('room_type')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    check_in = request.GET.get('check_in')
    check_out = request.GET.get('check_out')
    
    if room_type:
        rooms = rooms.filter(room_type=room_type)
    if min_price:
        rooms = rooms.filter(price__gte=min_price)
    if max_price:
        rooms = rooms.filter(price__lte=max_price)
    if check_in and check_out:
        rooms = rooms.exclude(booking__check_in__lt=check_out, booking__check_out__gt=check_in)

    return render(request, 'room_list.html', {'hotel': hotel, 'rooms': rooms})

def booked_rooms(request):
    bookings = Booking.objects.all()
    city = request.GET.get('city')
    if city:
        bookings = bookings.filter(room__hotel__city__icontains=city)
    return render(request, 'booked_rooms.html', {'bookings': bookings})






def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    bookings = Booking.objects.all()
    if request.method == 'POST':
        user_name = request.POST['user_name']
        user_phone = request.POST['user_phone']
        check_in = request.POST['check_in']
        check_out = request.POST['check_out']
        total_price = (room.price * (datetime.strptime(check_out, '%Y-%m-%d') - datetime.strptime(check_in, '%Y-%m-%d')).days).quantize(decimal.Decimal('0.01'))
        
        
        if total_price > 0 : 
        
            Booking.objects.create(
                room=room,
                user_name=user_name,
                user_phone=user_phone,
                check_in=check_in,
                check_out=check_out,
                total_price=total_price
            )
            
        else: return redirect("home")
        return redirect('booked_rooms')
    
    return render(request, 'book_room.html', {'room': room, 'bookings':bookings})

def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.delete()
    return redirect("/")


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer