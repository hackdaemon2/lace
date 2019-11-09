from datetime import datetime
from django.utils import timezone
from django.conf import settings

def get_error_class():
    error_css_class = 'alert alert-danger' 
    return error_css_class

def get_global_context():
    context = {}
    context['current_year'] = timezone.now().year
    context['app_name'] = settings.APP_NAME
    context['support_email'] = settings.SUPPORT_EMAIL
    context['support_phone'] = settings.SUPPORT_PHONE
    context['address'] = settings.ADDRESS
    return context

def extra_context(context, title):
    context.update(get_global_context())
    context['title'] = title
    return context
