from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View

from shop.cart import Cart
from .forms import RegisterForm


# logged in user page: /user

@login_required
def user(request):
    return render(request, 'users/user.html', {})


# register new user: /user/register
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        # register form
        if form.is_valid():
            form.save()
            messages.success(request, "Uživatel byl úspěšně zaregistrován!")

            # if successfully registered
            return redirect('login')

    else:
        form = RegisterForm()

    return render(
        request,
        'users/register.html',
        {
            'form': form
        })
