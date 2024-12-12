# myapp/forms.py
from django import forms
from django.contrib.auth.models import User
from . models import UserProfileInfo

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Password and confirm password do not match.")
        return confirm_password

class UserProfileInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfileInfo
        fields = ['name', 'image', 'email', 'phone', 'about']