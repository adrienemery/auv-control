"""auv_control URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from .views import Status


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^status/', Status.as_view()),
    url(r'^api/auth/', include('knox.urls')),
    url(r'^api/auth/', include('authenticator.urls')),
    url(r'^api/', include('djoser.urls.base')),
    url(r'^api/auth/', include('djoser.urls.authtoken')),
    url(r'^api/', include('auv.urls')),
    url(r'^api/', include('navigation.urls')),
]
