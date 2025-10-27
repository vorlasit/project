# models.py

from django.db import models
from django.contrib.auth.models import User
from inventory.models import Product
from res.models import CustomUser,BaseModel  
from store.models import Store


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1) 
    @property
    def total(self):
        return self.product.price * self.quantity
    
class Order(BaseModel):
    STATE_CHOICES = [
        ('not_paid', 'Not Paid'),
        ('paid', 'Paid'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
    total = models.DecimalField(max_digits=10, decimal_places=2)
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default='not_paid')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    def save(self, *args, **kwargs):
        # Auto set store from product if not provided
        if not self.store:
            self.store = self.product.store
        if not self.price:
            self.price = self.product.price
        self.subtotal = self.price * self.quantity
        super().save(*args, **kwargs)
class Payment(BaseModel):
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('transfer', 'Bank Transfer'),
        ('card', 'Credit/Debit Card'),
    ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    reference = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_slip = models.ImageField(upload_to='payment_slips/', null=True, blank=True)

class Paymentlist(models.Model): 
    Payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='paymentlists')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    
    
