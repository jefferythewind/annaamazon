from django.conf.urls import url

from . import views

app_name = 'data'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^grouped_orders/', views.grouped_orders, name='grouped_orders'),
    url(r'^orders/', views.orders, name='orders'),
    url(r'^all_data/', views.all_data, name='all_data'),
    url(r'^cd_items/', views.cd_items, name='cd_items'),
    url(r'^inactive/', views.inactive, name='inactive'),
]