"""lace URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.conf.urls import url
from user_auth import views, api_views

app_name = 'auth'
urlpatterns = [
    path('', views.IndexView.as_view(), name=views.IndexView.name),
    path('privacy-policy/', views.PrivacyPolicyView.as_view(), name=views.PrivacyPolicyView.name),
    path('cookie-policy/', views.CookiePolicyView.as_view(), name=views.CookiePolicyView.name),
    path("users/", api_views.UserListAPIView.as_view(), name=api_views.UserListAPIView.name),
    # path("auth/signup/", views.AuthUserCreateView.as_view(), name=views.AuthUserCreateView.name),
    path("auth/create-account/", api_views.UserCreateAPIView.as_view(), name=api_views.UserCreateAPIView.name),
    path("auth/login/", api_views.LoginAPIView.as_view(), name=api_views.LoginAPIView.name),
    path('auth/password-reset/', api_views.PasswordResetAPIView.as_view(), name=api_views.PasswordResetAPIView.name),
    url(r'^auth/password-reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.AuthPasswordResetConfirmView.as_view(), name=views.AuthPasswordResetConfirmView.name),
    url(r'^auth/verify-email/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.VerifyEmailView.as_view(), name=views.VerifyEmailView.name),
    path('auth/password-reset/complete/', views.AuthPasswordResetCompleteView.as_view(), name=views.AuthPasswordResetCompleteView.name),
]
