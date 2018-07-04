from django.conf.urls import url

from . import views

app_name = 'satellite'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'tm/$', views.tm, name='tm'),
    url(r'tm/errors$', views.errors, name='errors'),
    url(r'tm/hello$', views.hello, name='hello'),
    url(r'tm/housekeeping$', views.housekeeping, name='housekeeping'),
    url(r'tm/upload_tm$', views.upload_tm, name='upload_tm'),
]
