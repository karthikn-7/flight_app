from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *


def signup_view(request):
    if request.method == "POST":
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        password = request.POST.get("password1")
        password2 = request.POST.get("password2")
        
        if password != password2:
            return render(request,'login_signup.html',{'message':"Password Doesn't Match!"})
        
        if SimpleUser.objects.filter(email=email).exists():
            return render(request,'login_signup.html',{'message':"Email Already Exists!"})
        
        user = SimpleUser.objects.create_user(email=email,fullname=fullname,password=password)

        login(request,user)
        return redirect("home")
    
    return render(request,"login_signup.html")



def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        user = authenticate(request,email=email,password=password)
        if user is not None:
            login(request,user)
            return redirect("home")
        else:
            return render(request,'login_signup.html',{"message":"Invalid Password or Email!"})
        
    return render(request, 'login_signup.html')



@login_required(login_url='login')
def user_home(request):
    from datetime import date
    min_departure_date = date.today().strftime('%Y-%m-%d')
    
    
    # change if you need : )
    cities = [
        "Delhi", "Mumbai", "Chennai", "Bangalore", "Hyderabad", "Kolkata", "Pune", "Ahmedabad", "Dubai", "London"
        ]
    airlines = [
        "Indigo", "Air India", "SpiceJet", "Vistara", "GoAir", "Emirates", "Qatar Airways", "British Airways"
    ]
    return render(request,'user_home.html',context={
        "cities" : cities, 
        "airlines" : airlines,
        "min_departure_date":min_departure_date,
        })
    

def user_logout(request):
    logout(request)
    return redirect("home")