from django.contrib.auth.forms import AuthenticationForm ,UserCreationForm
from django import forms
from .models import CustomUser, AppSettings,GroupProfile
from django.contrib.auth.models import Group,Permission

class GroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all().order_by('content_type__app_label', 'codename'),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Permissions",
    )
    avatar = forms.ImageField(required=False, label="Group Avatar")

    class Meta:
        model = Group
        fields = ['name', 'permissions']  # name + permissions

    def save(self, commit=True):
        group = super().save(commit)
        avatar = self.cleaned_data.get('avatar') 

        profile, created = GroupProfile.objects.get_or_create(group=group)
        if not avatar and profile.avatar:
            profile.avatar.delete(save=False)  # ลบไฟล์จริง
            profile.avatar = None
        if avatar:
            profile.avatar = avatar

        profile.save()
        return group

class AppSettingsForm(forms.ModelForm):

    class Meta:
        model = AppSettings
        fields = ["name", "favicon", "app_icon"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Application Name'}),
            }
     
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Password'
    }))
    
class EditUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Email'
    }))
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Phone'
    }))
    avatar = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={
        'class': 'form-control'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Username'
    }))
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'})
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'avatar','groups']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.phone = self.cleaned_data.get('phone')
        avatar = self.cleaned_data.get('avatar')
        if avatar and user.avatar:
            user.avatar.delete(save=False)  # ลบไฟล์จริง
            user.avatar = None
        if commit:
            user.save() 
            self.save_m2m()  # ต้องเรียกเพื่อบันทึก M2M
            user.groups.set(self.cleaned_data['groups'])  # ✅ บันทึก group
        return user

    def __init__(self, *args, **kwargs): 
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs) 
        if not user or not user.groups.filter(name__iexact='Administrator').exists():
            self.fields['groups'].queryset = Group.objects.exclude(name__iexact='Administrator')
        else:
            self.fields['groups'].queryset = Group.objects.all()

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Email'
    })) 
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Phone'
    }))
    avatar = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={
        'class': 'form-control'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Username'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Password'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirm Password'
    }))
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'})
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'avatar', 'password1', 'password2','groups']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.phone = self.cleaned_data.get('phone')
        user.avatar = self.cleaned_data.get('avatar')   
        if commit:
            user.save() 
            # ✅ Get selected groups
            selected_groups = self.cleaned_data.get('groups')

            if selected_groups:
                user.groups.set(selected_groups)
            else: 
                default_group, created = Group.objects.get_or_create(name='User')
                user.groups.add(default_group)
        return user
    def __init__(self, *args, **kwargs):
        # accept optional `user` kwarg so we can filter group choices
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        all_groups = Group.objects.all().order_by('id')

        # ✅ ถ้า user ไม่มีสิทธิ์ Administrator -> ซ่อนกลุ่มแรก
        if not user or not user.groups.filter(name__iexact='Administrator').exists():
            if all_groups.exists():
                all_groups = all_groups[1:]

        self.fields['groups'].queryset = all_groups

        # ✅ ตั้งค่า default group = "Customer" ถ้ามี
        default_group = Group.objects.filter(name__iexact="Customer")
        if default_group.exists():
            self.fields['groups'].initial = default_group
            
class RegisterNoneLogForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Email'
    })) 
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Phone'
    }))
    avatar = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={
        'class': 'form-control'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Username'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Password'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirm Password'
    }))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'avatar', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.phone = self.cleaned_data.get('phone')
        user.avatar = self.cleaned_data.get('avatar')   

        if commit:
            user.save() 
            selected_groups = self.cleaned_data.get('groups')

            if selected_groups:
                user.groups.set(selected_groups)
            else: 
                default_group, created = Group.objects.get_or_create(name='User')
                user.groups.add(default_group)  # ✅ correct usage
        return user      
    
class GroupSelectForm(forms.ModelForm):
    groups = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = CustomUser
        fields = ['groups']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if not user or not user.groups.filter(name__iexact='Administrator').exists():
            self.fields['groups'].queryset = Group.objects.exclude(name__iexact='Administrator')

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()
            group_obj = self.cleaned_data.get('groups')
            if group_obj:
                user.groups.set([group_obj])  # ✅ wrap single Group in list
        return user
    