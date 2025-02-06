from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Flight, Booking
from django.contrib import messages
import random

def resched_cancel_view(request):
    return render(request,'public/resched_cancel.html')


@login_required(login_url='login')
def boardingPass_view(request):
    # bookings = Booking.objects.filter(user=request.user).order_by("-id")
    bookings = Booking.objects.filter(user=request.user).order_by("-id")
    
    if not bookings.exists():
        return render(request,'public/boarding.html',{"message":"No Bookings Found!"})
        
    return render(request,'public/boarding.html',{
        "bookings":bookings,
        "seat_number":random.randint(1, 50),
    })

@login_required(login_url='login')
def payment_view(request):
    
    flight_data = request.session.get("flight_data")

    if not flight_data:
        return redirect("book_flight")

    if request.method == "POST":
        request.session["payment_success"] = True
        return redirect("confirm_booking")

    return render(request, "public/payment.html", {"flight": flight_data})


@login_required(login_url='login')
def confirm_booking(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('login')
        
        flight_data = request.session.get('flight_data')
        
        if not flight_data:
            return redirect('user_home')
        
        from datetime import time
        boarding_time = time(random.randint(0,23),random.randint(0,59))
        flight = Flight.objects.create(
            fullname = flight_data['fullname'],
            age = flight_data['age'],
            gender = flight_data['gender'],
            airline = flight_data['airline'],
            flight_number = flight_data['flight_number'],
            departure = flight_data['departure'],
            destination=flight_data["destination"],
            departure_date=flight_data["departure_date"],
            return_date=flight_data["return_date"],
            class_type=flight_data["class_type"],
            boarding_time=boarding_time
        )
        
        booking = Booking.objects.create(user=request.user, flight=flight)
        
        del request.session["flight_data"]
        amount = random.randint(3000, 5000)
        return render(request, "public/booking.html", {
            "booking":booking,
            "booking_reference":booking.id,
            "message": "Booking Confirmed!",
            "amount": amount })
    
    flight_data = request.session.get("flight_data", {})
    return render(request,'public/booking.html',{"flight":flight_data})


@login_required(login_url='login')
def book_flight(request): 
    if request.method == "POST":
        
        if not request.user.is_authenticated:
            return redirect('login')
        
        flight_data = {
            "fullname": request.POST.get("fullname"),
            "age": request.POST.get("age"),
            "gender": request.POST.get("gender"),
            "airline": request.POST.get("airline"),
            "departure": request.POST.get("departure"),
            "destination": request.POST.get("destination"),
            "departure_date": request.POST.get("departure-date"),
            "return_date": request.POST.get("return-date"),
            "class_type": request.POST.get("class"),
        }
        
        airline_code = flight_data["airline"][:2].upper()
        flight_data["flight_number"] = f"{airline_code}{random.randint(100, 999)}"
        
        request.session["flight_data"] = flight_data
        
        
        return redirect("payments")
    
    return render(request, 'public/booking.html')

@login_required(login_url='login')
def cancel_flight(request):
    if request.method == "POST":
        reference_no = request.POST.get("booking_reference")
        
        booking = Booking.objects.filter(id=reference_no,user=request.user).first()
        
        if booking:
            booking.delete()
            messages.success(request,"Your flight booking has been successfully canceled.")
        else:
            messages.error(request,"Booking not found! Check Your Reference Number!")
        return redirect("reschedules")

@login_required(login_url='login')
def reschedule_flight(request):
    if request.method == "POST":
        reference_number = request.POST.get('booking_reference')
        new_departure_date = request.POST.get('new_date')
        
        booking = Booking.objects.filter(id=reference_number,user=request.user).first()
        
        if booking:
            booking.flight.departure_date = new_departure_date
            booking.flight.save()
            messages.success(request,"Flight has been rescheduled succesfully!")
        else:
            messages.error(request,"Booking not found! Check Your Reference Number!")
        return redirect('reschedules')

# Non functional page
def aboutUs_view(request):
    return render(request,'public/about.html')