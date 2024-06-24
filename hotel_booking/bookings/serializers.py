from rest_framework import serializers
from .models import Hotel, Room, Booking

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['id', 'name', 'city', 'description', 'image']

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'hotel', 'room_type', 'price', 'available', 'image']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'room', 'user_name', 'user_phone', 'check_in', 'check_out', 'total_price', 'status']
