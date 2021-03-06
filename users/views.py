from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages


def register(request):
    if request.method == "POST":
        # instantiate form with the post data.
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # cleaned data gets nicely formatted data in Python objects.
            username = form.cleaned_data.get("username")
            messages.success(
                request, f"Your account has been created! You are now able to log in!"
            )
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})