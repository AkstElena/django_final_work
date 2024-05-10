from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import LoginUserForm


class LoginUser(LoginView):
    form_class = LoginUserForm
    authentication_form = LoginUserForm
    template_name = 'userapp/login.html'
    extra_context = {'title': 'Авторизация'}


# def login_user(request):
#     if request.method == "POST":
#         form = LoginUserForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'], password=cd['password'])
#             if user and user.is_active:
#                 login(request, user)
#                 return redirect('index')
#     else:
#         form = LoginUserForm()
#     return render(request, 'userapp/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('userapp:login')
