"""
URL configuration for mysite project.

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
from django.contrib import admin
from django.urls import include, path
from stream.views import camera_feed

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api_users/", include("users.urls")),
    path("api_parking/", include("parking.urls")),
    path("api_quan_tri_vien/", include("quan_tri_vien.urls")),
    path("connect_esp8266/",include("connect_esp8266.urls")),
    path('video_feed/', camera_feed, name='video_feed')
]
