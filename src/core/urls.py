"""
URL configuration for lms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.urls import path

from core.views import (
    index,
    error_400,
    error_404,
    error_403,
    error_429,
    error_500,
    error_503,
)

app_name = "core"

urlpatterns = [

    path('', index, name='index'),
]

handler400 = error_400
handler403 = error_403
handler404 = error_404
handler429 = error_429
handler500 = error_500
handler503 = error_503
