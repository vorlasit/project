from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.product_create_view, name='product_create'),
    path('list/', views.product_list_view, name='product_list'),
    path('edit/<int:pk>/', views.product_edit, name='product_edit'),
    path('delete/<int:pk>/', views.product_delete, name='product_delete'),
    # เพิ่ม URL patterns อื่นๆ ตามต้องการ
]