from django.urls import path
from . import views

urlpatterns = [
    # -----------------------
    # User wallet views
    # -----------------------
    path('wallet/', views.wallet_detail, name='wallet_detail'),
    path('wallet/deposit/', views.deposit, name='wallet_deposit'),
    path('wallet/withdraw/', views.withdraw, name='wallet_withdraw'),

    # -----------------------
    # Admin wallet views
    # -----------------------
    path('admin/users/', views.admin_user_list, name='admin_user_list'), 
    path('admin/users/<int:user_id>/deposit/', views.admin_deposit_user, name='deposit'),
    path('admin/users/<int:user_id>/withdraw/', views.admin_withdraw_user, name='withdraw'),
]
