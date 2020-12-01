"""BBS2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from BBS2 import settings
from app01 import views
from django.views.static import serve
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home',views.home,name='home'),
    url(r'^register/',views.register,name='register'),
    url(r'^login/',views.login,name='login'),
    url(r'^get_code/',views.get_code),
    #url(r'^blog/',views.blog),
    url(r'^up_down/',views.up_down),
    url(r'^(?P<username>\w+)/article/(?P<article_id>\d+)/',views.article),
    url(r'^media/(?P<path>.*)',serve,{'document_root':settings.MEDIA_ROOT}),
    #个人站点
    url(r'^(?P<username>\w+)/$',views.blog),
    #个人站点侧边栏筛选功能
    url(r'^(?P<username>\w+)/(?P<condition>classify|tag|time_classify)/(?P<param>.*)/',views.blog),
    #url(r'^(?P<username>\w+)/(?P<condition>category|tag|archive)/(?P<param>.*)/',views.site),


]
