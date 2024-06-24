
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HotelViewSet, RoomViewSet, BookingViewSet



router = DefaultRouter()
router.register(r'hotels', HotelViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('api/', include(router.urls)),
    path('hotels/', views.hotel_list, name='hotel_list'),
    path('rooms/<int:hotel_id>/', views.room_list, name='room_list'),
    path('booked-rooms/', views.booked_rooms, name='booked_rooms'),
    path('book-room/<int:room_id>/', views.book_room, name='book_room'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]
