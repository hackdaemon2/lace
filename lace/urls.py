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
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.static import serve
# from rest_framework_simplejwt import views as jwt_views
# from user_auth.admin import admin_site

# urlpatterns = []

urlpatterns = [
    path( '', include( 'user_auth.urls', namespace = 'auth' ) ),
    path( '', include( 'dashboard.urls', namespace = 'dashboard' ) ),
    # path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh')
    # path( 'dashboard', include( 'dashboard.urls', namespace = 'dashboard' ) ),
    # path('console/', admin_site.urls),
    # url('', include('pwa.urls')), # You MUST use an empty string as the URL prefix
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
