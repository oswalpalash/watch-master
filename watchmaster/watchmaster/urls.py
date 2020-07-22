from __future__ import absolute_import, unicode_literals
"""watchmain URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url,include
from django.contrib import admin
from check.views import send_ping,plot,index,test_ping,check_loading_time,stress_test
from subordinates.views import add
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^subordinate/', include('subordinates.urls')),
    url(r'^$', index),
    url(r'^add',add),
    url(r'^ping',send_ping),
    url(r'^test_ping', test_ping),
    url(r'^plot',plot),
    url(r'^load',check_loading_time),
    url(r'^stress',stress_test),
]
