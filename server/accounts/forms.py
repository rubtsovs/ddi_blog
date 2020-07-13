from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True,
                            widget=forms.EmailInput())
    avatar = forms.ImageField(required=True)

    class Meta:
        model = User
        fields = ('avatar', 'first_name', 'last_name',
                  'email', 'password1', 'password2')
