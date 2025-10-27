from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import StoreForm
from .models import Store
from sale.models import OrderItem
from django.contrib import messages
from django.shortcuts import get_object_or_404
from sale.models import Order

@login_required
def store_create_view(request):
    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            store = form.save(commit=False)
            store.create_uid = request.user     # ✅ ต้องเป็น object ไม่ใช่ id
            store.write_uid = request.user 
            store.save()
            messages.success(request, "Store created successfully.")
            return redirect('store_list')
    else:
        form = StoreForm()
    return render(request, 'store_form.html', {'form': form})



@login_required
def store_edit_view(request, pk):
    store = get_object_or_404(Store, pk=pk)
    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES, instance=store, user=request.user)
        if form.is_valid():
            store = form.save(commit=False)
            store.write_uid = request.user
            store.save()
            messages.success(request, "Store updated successfully.")
            return redirect('store_list')
    else:
        form = StoreForm(instance=store, user=request.user)
    return render(request, 'store_form.html', {'form': form})

def store_list_view(request):
    # ดึงข้อมูลร้านค้าทั้งหมด
    stores = Store.objects.all()
    return render(request, 'store_list.html', {'stores': stores})
@login_required
def store_delete_view(request, pk):
    store = get_object_or_404(Store, pk=pk)
    if request.method == 'POST':
        store.delete()
        messages.success(request, "Store deleted successfully.")
        return redirect('store_list')
    return render(request, 'store_confirm_delete.html', {'store': store})

@login_required 
def store_detail(request, store_id): 
    store = get_object_or_404(Store, id=store_id)

    # ดึง OrderItem ทั้งหมดของร้านนี้ พร้อมข้อมูล order และสินค้า
    order_items = store.orders.select_related('order', 'product')

    return render(request, 'store_detail.html', {
        'store': store,
        'order_items': order_items
    })