from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.cart_view, name='cart_view'),
    path('create_order/', views.create_order, name='create_order'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<str:status>/', views.order_list, name='order_list'),  # 👈 รองรับ filter

    path('order/<int:order_id>/payment/', views.create_payment, name='create_payment'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order_user/<int:user_id>/', views.order_user_view, name='order_user_view'),
    

 
    path('payment/<int:payment_id>/', views.payment_detail_view, name='payment_detail'),
    path('payments/', views.payment_list_view, name='payment_list'),
    path('order_line/', views.order_line, name='order_line'),
    
    
    path('qr/<int:order_id>/', views.generate_qr, name='bank_generate_qr'),
    path('done/<int:order_id>/', views.payment_done, name='bank_payment_done'),

]
