from django.urls import path
from . import views
 

urlpatterns = [
    path('create/', views.store_create_view, name='store_create'),
    path('<int:store_id>/', views.store_detail, name='store_detail'),  # ✅ เพิ่มตรงนี้
    path('list/', views.store_list_view, name='store_list'),
    path('stores/<int:pk>/edit/', views.store_edit_view, name='store_edit'),
    path('stores/<int:pk>/delete/', views.store_delete_view, name='store_delete'),
    
    # เพิ่ม URL patterns อื่นๆ ตามต้องการ
]
 