from django import forms 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from app.models import CustomUser

class CustomUserCreateForm(UserCreationForm):
    """docstring for CustomUserCreateForm"""
    class Meta:
        model = CustomUser
        fields = ['email']
        exclude = ['username']


class CustomUserChangeForm(UserChangeForm):
    """docstring for CustomUserChangeForm"""
    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        del self.fields['username']

        class Meta:
            model = CustomUser
 

class Search(forms.Form):
    search = forms.CharField(required=False, label='')


class UserSignUp(forms.Form):
    """docstring for UserSignUp"""
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(required=False, label='Re-enter password please', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    next_page = forms.CharField( required=False, widget=forms.HiddenInput())


class UserLogin(forms.Form):
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    next_page = forms.CharField( required=False, widget=forms.HiddenInput())


class ContactForm(forms.Form):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'name', 'placeholder': "Enter name",  'title': "Please enter your name (at least 2 characters)", 'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'id': 'email', 'placeholder': "Enter email", 'title': "Please enter a valid email address", 'class': 'form-control'}))
    phone = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'phone', 'class':"form-control required digits", 'type':"tel", 'size':"30", 'value':"", 'placeholder':"Enter phone", 'title':"Please enter a valid phone number (at least 10 characters)"}))
    message = forms.CharField(required=True, widget=forms.Textarea(attrs={'id': 'message', 'class': "message form-control", 'cols': "3", 'rows': "5", 'placeholder': "Enter your message...", 'title': "Please enter your message (at least 10 characters)"}))
