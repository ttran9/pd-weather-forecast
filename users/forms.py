from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        # specify the model that this form interacts with.
        # when the form validates it creates a new user.
        model = User
        fields = ["username", "email", "password1", "password2"]
