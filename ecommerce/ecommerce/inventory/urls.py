from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.product_create_or_edit, name='product_create'),
    path('list/', views.product_list_view, name='product_list'),
    path('edit/<int:pk>/', views.product_create_or_edit, name='product_edit'),
    path('delete/<int:pk>/', views.product_delete, name='product_delete'),
    path('<int:pk>/add-file/', views.product_add_file, name='product_add_file'),
    # เพิ่ม URL patterns อื่นๆ ตามต้องการ
    
    # path('cart/', views.cart_view, name='cart_view'),
    # path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    # path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    # add to cart URLs
]