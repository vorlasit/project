from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from .form import (RegisterForm, 
                   EditUserForm, 
                   AppSettingsForm, 
                   GroupSelectForm,
                   RegisterNoneLogForm,
                   GroupForm)
from django.contrib.auth import login, logout
from .models import CustomUser,AppSettings,GroupProfile
from django.contrib.auth.models import Group,Permission
from sale.models import Order, Payment
from inventory.models import Product
from django.db.models import Sum
 
from django.utils.timezone import now
from datetime import timedelta
import calendar

def settings_view(request):
    settings = AppSettings.get_settings()
    if request.method == "POST":
        form = AppSettingsForm(request.POST, request.FILES, instance=settings)
        if form.is_valid():
            form.save()
        return redirect("settings")  # reload after save
    else:
        form = AppSettingsForm(instance=settings)

    icons = AppSettings.objects.all()

    return render(request, "setting.html", {"form": form, 'icons':icons})


@login_required
def group_list_view(request):
    groups = Group.objects.all()
    return render(request, 'group_list.html', {'groups': groups})

@login_required
def group_create_view(request):
    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Group created successfully.")
            return redirect('group_list')
    else:
        form = GroupForm()

    return render(request, 'group_form.html', {'form': form})



@login_required
def group_edit_view(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, "Group updated successfully.")
            return redirect('group_list')
    else:
        form = GroupForm(instance=group)
    return render(request, 'group_form.html', {'form': form, 'group': group})

# 🗑️ ลบกลุ่ม
@login_required
def group_delete_view(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group.delete()
    messages.success(request, "Group deleted successfully.")
    return redirect('group_list')

@login_required
def dashboard(request):
    total_orders = Order.objects.count()
    total_paid_orders = Order.objects.filter(state='paid').count()
    total_products = Product.objects.count()
    total_users = CustomUser.objects.count()
    total_payment = Payment.objects.aggregate(total=Sum('amount'))['total'] or 0

    # Orders per month (last 12 months)

    last_12_months = []
    order_counts = []

    for i in range(11, -1, -1):
        month = now() - timedelta(days=i*30)  # approximate month
        month_start = month.replace(day=1)
        month_end = month.replace(day=calendar.monthrange(month.year, month.month)[1])
        count = Order.objects.filter(created_at__range=(month_start, month_end)).count()
        last_12_months.append(month.strftime('%b %Y'))
        order_counts.append(count)

    # Payment per method
    payment_method_summary = Payment.objects.values('method').annotate(total=Sum('amount'))

    context = {
        'total_orders': total_orders,
        'total_paid_orders': total_paid_orders,
        'total_products': total_products,
        'total_users': total_users,
        'total_payment': total_payment,
        'order_chart_labels': last_12_months,
        'order_chart_data': order_counts,
        'payment_method_summary': payment_method_summary,
    }

    return render(request, 'dashboard.html', context) 

@login_required
def edit_user(request):
    user = request.user
    if request.method == 'POST':
        form = EditUserForm(request.POST, request.FILES, instance=user, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('edit_user')  
    else:
        form = EditUserForm(instance=user, user=request.user)

    return render(request, 'edit_user.html', {'form': form})


@login_required
def edit_user_list(request, pk):
    edit_user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = EditUserForm(request.POST, request.FILES, instance=edit_user, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = EditUserForm(instance=edit_user, user=request.user)

    return render(request, 'edit_user.html', {'form': form})

def register_view(request): 
    user = request.user
    if request.method == 'POST': 
        form = RegisterForm(request.POST, request.FILES, user=user)        
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm(user=user)
    return render(request, 'register.html', {'form': form })

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def user_list_view(request):
    users = CustomUser.objects.all()
    groups = Group.objects.all()
    return render(request, 'user_list.html', {'users': users,
        "groups": groups,})

# -----------------------------
# Step 1: Register user (no login yet)
# -----------------------------
def registernonelog(request):
    if request.method == 'POST':
        form = RegisterNoneLogForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Redirect to Step 2 (group selection)
            return redirect('select_group', user_id=user.id)
    else:
        form = RegisterNoneLogForm()
    
    return render(request, 'register_not_log.html', {'form': form})
# -----------------------------
# Step 2: Select group (after registration)
# -----------------------------
def select_group_view(request, user_id):
    user_obj = get_object_or_404(CustomUser, id=user_id) 
    form = GroupSelectForm(request.POST or None, instance=user_obj, user=request.user) 
    groups = form.fields['groups'].queryset 
    if request.method == 'POST' and form.is_valid():
        form.save()
        login(request, user_obj)
        return redirect('dashboard')

    return render(request, 'select_group.html', {
        'form': form,
        'groups': groups,
        'user_obj': user_obj
    })
    
    