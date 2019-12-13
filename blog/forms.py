from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Post, Ainews


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)


class SignupForm(ModelForm):
    password_check = forms.CharField(max_length=200, widget=forms.PasswordInput())
    field_order = ['username', 'password', 'password_check', 'last_name', 'first_name', 'email']

    class Meta:
        model = User
        widgets = {'password': forms.PasswordInput}
        fields = ['username', 'password', 'last_name', 'first_name', 'email']

'''
class SigninForm(ModelForm):
    class Meta:
        model = User
        widgets = {'password': forms.PasswordInput}
        field = ['username', 'password']
'''


class AinewsForm(ModelForm):

    class Meta:
        model = Ainews
        fields = ('title', 'text', 'image',)
