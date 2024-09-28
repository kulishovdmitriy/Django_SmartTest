"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


API_PREFIX = 'api/v1'

urlpatterns = [
    # UI
    path('admin/', admin.site.urls),

    path('', include('core.urls')),

    path('accounts/', include('accounts.urls')),

    path('tests/', include('smart_test.urls')),

    # API
    path('api-auth/', include('rest_framework.urls')),

    path(f'{API_PREFIX}/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    path(f'{API_PREFIX}/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),

    path(f'{API_PREFIX}/smart_test/', include('smart_test.api.urls')),

    path(f'{API_PREFIX}/accounts/', include('accounts.api.urls')),
]

urlpatterns += \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
