from django import forms
from res.models import CustomUser as User

class DepositForm(forms.Form):
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0.01, label="Deposit Amount")

class WithdrawForm(forms.Form):
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0.01, label="Withdrawal Amount")

class AdminDepositForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), label="Select User")
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0.01, label="Deposit Amount")
    description = forms.CharField(max_length=255, required=False, label="Description")

class AdminWithdrawForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), label="Select User")
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0.01, label="Withdrawal Amount")
    description = forms.CharField(max_length=255, required=False, label="Description")