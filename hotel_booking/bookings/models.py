from django.db import models

class Hotel(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='hotels/')

    def __str__(self):
        return self.name

class Room(models.Model):
    ROOM_TYPES = [
        ('single', 'Single Room'),
        ('double', 'Double Room'),
        ('deluxe', 'Deluxe Room'),
    ]

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_type = models.CharField(max_length=50, choices=ROOM_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='rooms/')

    def __str__(self):
        return f"{self.hotel.name} - {self.get_room_type_display()}"

class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255)
    user_phone = models.CharField(max_length=20)
    check_in = models.DateField()
    check_out = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='Booked')

    def __str__(self):
        return f"Booking: {self.room.hotel.name} - {self.room.get_room_type_display()} by {self.user_name}"
