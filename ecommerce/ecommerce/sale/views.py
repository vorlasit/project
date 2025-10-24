from django.shortcuts import render ,redirect, get_object_or_404
from .models import Cart,CartItem, Order, OrderItem,Payment,Paymentlist
from django.contrib.auth.decorators import login_required
from inventory.models import Product, ProductFile
from django.contrib import messages
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    # ดึงหรือสร้าง cart สำหรับ user ปัจจุบัน
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # ดึงจำนวนจาก query หรือใช้ค่า default = 1
    try:
        quantity = int(request.GET.get('quantity', 1))
        if quantity <= 0:
            quantity = 1
    except ValueError:
        quantity = 1

    # ดึงหรือสร้าง CartItem
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )

    # ถ้าเคยมีอยู่แล้ว → บวกเพิ่ม
    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    return redirect('cart_view')
@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()  # ✅ ต้องใส่ .all()

    total = sum(item.total for item in items)

    return render(request, 'cart.html', {
        'cart': cart,
        'items': items,
        'total': total
    })
    
@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('cart_view')
 
def mark_order_paid(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.state = 'paid'
    order.save()
    return redirect('order_detail', order_id=order.id)
@login_required
def create_order(request):
    cart = get_object_or_404(Cart, user=request.user)
    if not cart.items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart')

    # Calculate total
    total_amount = sum(item.product.price * item.quantity for item in cart.items.all())

    # Create order
    order = Order.objects.create(
        user=request.user,
        state='not_paid',
        total=total_amount
    )

    # Move items
    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price,
            subtotal=item.product.price * item.quantity
        )

    # Clear cart
    cart.items.all().delete()

    return redirect('order_detail', order.id)

@login_required
def order_list(request):
    # show orders only for the logged-in user
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_list.html', {'orders': orders})

def mark_order_paid(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.state = 'paid'
    order.save()
    return redirect('order_detail', order.id)


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = order.items.all()  # assuming OrderItem model has related_name='items'
    payments = order.payments.all()  # ถ้ามีการชำระเงินแล้ว

    total = sum(item.subtotal for item in items)
    
    return render(request, 'order_detail.html', {
        'order': order,
        'items': items,
        'payments': payments,
        'total': total,
    })
    


@login_required
def payment_list_view(request):
    payments = Payment.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'payment_list.html', {'payments': payments}) 

@login_required
def payment_detail_view(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    paymentlists = payment.paymentlists.all()  # assuming related_name='paymentlists'

    return render(request, 'payment_detail.html', {
        'payment': payment,
        'paymentlists': paymentlists,
    })

@login_required
def create_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == 'POST':
        amount = float(request.POST.get('amount', order.total))
        method = request.POST.get('method', 'cash')
        reference = request.POST.get('reference', '')
        payment_slip = request.FILES.get('avatar')

        # Create main Payment
        payment = Payment.objects.create(
            order=order,
            user=request.user,
            amount=amount,
            method=method,
            reference=reference,
            payment_slip=payment_slip,
        )

        # Move order items into Paymentlist
        for item in order.items.all():
            Paymentlist.objects.create(
                Payment=payment,
                user=request.user,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
                subtotal=item.product.price * item.quantity
            )

        # Update order status
        order.state = 'paid'
        order.save()

        return redirect('order_detail', order.id)

    return render(request, 'create_payment.html', {'order': order})