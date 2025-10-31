# bank/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('balance/', views.get_balance),
    path('deposit/', views.deposit),
    path('withdraw/', views.withdraw),
    path('transfer/', views.transfer),
    path('pay/', views.pay_order),
]
