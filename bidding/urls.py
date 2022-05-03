"""bidding URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from items.views import *

from items.views import login_user

urlpatterns = [
    path('admin/', admin.site.urls),

    # path('login_user/', login_user,"login_user"),
    path('', login_user, name='login_user'),
    path('home/', home, name='home'),
    path('register/', register, name='register'),
    path('logout/', logoutUser, name='logoutUser'),
    path('single-item/<id>/', singleitem, name='singleitem'),
    path('items/', item_report, name='item_report'),
    path('lowest/<item>/', lowest_bidder, name='lowest_bidder'),





]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
