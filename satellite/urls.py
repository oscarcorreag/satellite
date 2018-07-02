from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^grid/$', views.grid_handler, name='grid_handler'),
    url(r'^cfg/$', views.grid_config, name='grid_config'),
]
