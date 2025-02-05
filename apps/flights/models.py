from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Flight(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_flights",null=True,blank=True)
    # Payanigal Infos
    fullname = models.CharField(max_length=100, null=False, verbose_name="Full Name")
    age = models.PositiveIntegerField(null=False, verbose_name="Age")
    GENDER_CHOICES = [
        ('Male','Male'),
        ('Female','Female'),
        ('Others','Others'),
    ]
    gender = models.CharField(max_length=20, null=False, choices=GENDER_CHOICES, verbose_name="Gender")
    
    # Vimana Infos
    airline = models.CharField(max_length=100, verbose_name="Airline")
    flight_number = models.CharField(max_length=20, unique=True, verbose_name="Flight Number")
    departure = models.CharField(max_length=100, verbose_name="Departure City")
    destination = models.CharField(max_length=100)
    
    # Date infos
    departure_date = models.DateField(null=False, verbose_name="Departure Date")
    return_date = models.DateField(null=True, blank=True, verbose_name="Return Date")
    class_type = models.CharField(max_length=20,null=True,verbose_name="Class")
    
    
    def __str__(self):
        return f"{self.airline} - {self.flight_number} ({self.departure} -> {self.destination})"
    
    
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="user_bookings")
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE,related_name="flight_bookings")
    booking_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Booking: {self.user.full_name} -> {self.flight.flight_number}"