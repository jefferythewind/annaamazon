from django.conf.urls import url

from . import views

app_name = 'data'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^all_data/', views.all_data, name='all_data'),
]