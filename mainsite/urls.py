from django.conf.urls import url

from . import views

app_name = 'mainsite'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^generic', views.generic, name='generic'),
    url(r'^elements', views.elements, name='elements'),
]