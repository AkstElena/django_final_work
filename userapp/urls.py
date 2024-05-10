from django.urls import path
from .views import LoginView, logout_user, ProfileUser, UserPasswordChange
from .forms import LoginUserForm, RegisterUserForm
from django.views.generic import CreateView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy

app_name = 'userapp'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='userapp/login.html', authentication_form=LoginUserForm,
                                     extra_context={'title': 'Авторизация'}), name='login'),
    path('logout/', logout_user, name='logout'),
    # path('register/', register, name='register'),
    path('register/', CreateView.as_view(template_name='userapp/register.html', form_class=RegisterUserForm,
                                         extra_context={'title': 'Регистрация'},
                                         success_url=reverse_lazy('userapp:login')), name='register'),
    path('profile/', ProfileUser.as_view(template_name='userapp/profile.html'), name='profile'),
    path('password-change/', UserPasswordChange.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name='userapp/password_change_done.html'),
         name='password_change_done'),
    path('password-reset/',
         PasswordResetView.as_view(template_name="userapp/password_reset_form.html",
                                   email_template_name="userapp/password_reset_email.html",
                                   success_url=reverse_lazy("userapp:password_reset_done")),
         name='password_reset'),
    path('password-reset/done/',
         PasswordResetDoneView.as_view(template_name="userapp/password_reset_done.html"),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name="userapp/password_reset_confirm.html",
                                          success_url=reverse_lazy("userapp:password_reset_complete")),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         PasswordResetCompleteView.as_view(template_name="userapp/password_reset_complete.html"),
         name='password_reset_complete'),
]
