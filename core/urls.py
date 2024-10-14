from django.urls import path, include
from .views import *
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('user_form/', Userform.as_view(), name='user-form'),
    path('sign_up/', SignupView.as_view(), name='sign-up'),
    path('sign_in/', SigninView.as_view(), name='sign-in'),
    path('logout',auth_views.LogoutView.as_view(), name='logout'),
    path('profile_update/<int:pk>/',ProfileUpdateView.as_view(), name='profile-update'),
    path('reset_password/',
         MyPasswordResetView.as_view(),
         name='reset_password'),
    path('reset/<uidb64>/<token>', PasswordResetConfirmView.as_view(
         template_name="password_reset_form.html"),
         name='password_reset_confirm'),
    path('change_password/<str:id>/', ChangePasswordView.as_view(), name='change_password'),
]