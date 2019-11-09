from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth import views as auth_views
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from dashboard.util_function import get_global_context
from django.utils.http import urlsafe_base64_decode
from . forms import AuthSetPasswordForm, AuthUserSignupForm, AuthUserLoginForm, AuthPasswordResetForm
from . tokens import verify_email_token

# Create your views here
class PrivacyPolicyView(TemplateView):
    name = 'privacy_policy'
    template_name = 'user_auth/privacy-policy.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update(get_global_context())
        return context
    
class CookiePolicyView(TemplateView):
    name = 'cookie_policy'
    template_name = 'user_auth/cookie-policy.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update(get_global_context())
        return context
    
class IndexView(TemplateView):
    name = 'index'
    template_name = 'user_auth/index.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update(get_global_context())
        context.update({'signup_form': AuthUserSignupForm})
        context.update({'login_form': AuthUserLoginForm()})
        context.update({'password_reset_form': AuthPasswordResetForm()})
        return context
    
class AuthLogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('user_auth:index')  
    
class AuthPasswordResetCompleteView(UserPassesTestMixin, TemplateView):
    name = 'password_reset_complete'
    template_name = 'user_auth/password_reset_complete.html'
    extra_context = get_global_context()
    
    def test_func(self):
        """Checks if the user is not authenticated.
        
        This performs a user test to ensure that the user has permission to view this page.
        The function checks if the user is not authenticated as only non-authenticated users 
        have the permission to view this page. Authenticated users cannot view this page.
        """
        is_unauthenticated_user = not self.request.user.is_authenticated
        return is_unauthenticated_user       

class AuthPasswordResetConfirmView(UserPassesTestMixin, auth_views.PasswordResetConfirmView):
    name = 'password_reset_confirm'
    template_name = 'user_auth/password_reset_confirm.html'
    form_class = AuthSetPasswordForm
    success_url = reverse_lazy('user_auth:password_reset_complete')    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_global_context())
        request_path = self.request.path.split('/')
        uidb64 = request_path[3] # the fourth index is the index that stores the uidb64 on the request path
        try:
            uid = force_text(urlsafe_base64_decode(uidb64).decode())
            user = get_user_model().objects.get(pk=uid)
        except (ValueError, TypeError, OverflowError, get_user_model().DoesNotExist):
            user = None
        if user is not None: 
            context['fullname'] = user.get_fullname().title()
        else:
            context['fullname'] = ' '.join([settings.APP_NAME.upper(), 'User'])
        return context
        
    def test_func(self):
        is_unauthenticated_user = not self.request.user.is_authenticated
        return is_unauthenticated_user
    
class VerifyEmailView(TemplateView):
    name = 'verify_email'
    template_name = 'user_auth/verify_email.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        uidb64 = kwargs.pop('uidb64')
        token = kwargs.pop('token')
        try:
            uid = force_text(urlsafe_base64_decode(uidb64).decode())
            user = get_user_model().objects.get(pk=uid)
        except (ValueError, TypeError, OverflowError, get_user_model().DoesNotExist):
            user = None
        if user is not None and verify_email_token.check_token(user, token):
            user.email_verified = True
            user.save()
            context['verification_status'] = True
            context['user_email'] = user.email
        else:
            context['verification_status'] = False
        context['support_email'] = settings.SUPPORT_EMAIL
        context['app_name'] = settings.APP_NAME
        return context