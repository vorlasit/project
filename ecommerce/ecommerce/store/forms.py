from .models import Store
from django import forms
from res.models import CustomUser

class StoreForm(forms.ModelForm):
    owner = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = Store
        fields = ['name', 'tel', 'owner', 'address', 'avatar']
        widgets = { 
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'tel': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    def __init__(self, *args, **kwargs):
        # รับ user จาก view
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # ถ้าไม่ใช่ admin group → ซ่อน owner field
        if self.user and not self.user.groups.filter(name='Administrator').exists():
            self.fields['owner'].widget = forms.HiddenInput()
            self.initial['owner'] = self.user