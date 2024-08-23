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

from accounts.views import AccountCreateView, AccountLoginView, AccountLogoutView, AccountUpdateView, UserListView

app_name = "accounts"

urlpatterns = [

    path('registration/', AccountCreateView.as_view(), name='registration'),

    path('login/', AccountLoginView.as_view(), name='login'),

    path('logout/', AccountLogoutView.as_view(), name='logout'),

    path('profile/', AccountUpdateView.as_view(), name='profile'),

    path('', UserListView.as_view(), name='list'),
]
