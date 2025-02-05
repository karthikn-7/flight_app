from django.urls import path
from .views import *

urlpatterns = [
    path('confirm_booking/',confirm_booking,name='confirm_booking'),
    path('boardings/',boardingPass_view,name='boardings'),
    path('payments/',payment_view,name='payments'),
    path('rechedules/',resched_cancel_view,name='reschedules'),
    path('aboutUs/',aboutUs_view,name='aboutUs'),
    path('book_flight/',book_flight,name='book_flight'),
    path('cancel_flight/',cancel_flight,name='cancel_flight'),
    path('reschedule_flight/',reschedule_flight,name='reschedule_flight')
]
