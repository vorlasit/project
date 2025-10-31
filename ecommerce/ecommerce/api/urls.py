from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import register_view, profile_view, login_view, order_list_view

urlpatterns = [ 
               path('register/', register_view, name='register'),
               path('login/', login_view, name='login'),
               path('profile/', profile_view, name='profile'),
               path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
               path('orders/', order_list_view, name='order_list'),
 ]
