from django import forms
from .models import Product, ProductFile
from store.models import Store

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'store']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4,'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'store': forms.Select(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # ต้องส่ง user จาก view
        super().__init__(*args, **kwargs)

        if self.user:
            user_stores = self.user.store_set.all()
 
            if user_stores.exists():
                # User มีร้านเป็น owner ให้เลือกร้านตัวเอง
                self.fields['store'].queryset = user_stores
                self.initial['store'] = user_stores.first()
                # self.fields['store'].widget.attrs['readonly'] = True
                # self.fields['store'].widget.attrs['disabled'] = True 
            else:
                # User ไม่มีร้าน ให้เลือกจากร้านว่าง (หรือจะ raise error)
                self.fields['store'].queryset = Store.objects.none()

class ProductFileForm(forms.ModelForm):
    class Meta:
        model = ProductFile
        fields = ['file']
