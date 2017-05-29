from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    #url(r'^update/$', views.update),
    #url(r'^data/(?P<i>\d+)/$', views.data),
    url(r'^fcfs/(?P<c>\d+)/$', views.fcfsData),
    url(r'^fcfsUpdate/$', views.fcfsUpdate, name = 'fcfsUpdate'),
    url(r'^staticPrior/(?P<c>\d+)/$', views.staticData),
    url(r'^staticUpdate/$', views.staticUpdate, name = 'staticUpdate'),
    url(r'^dynamicPrior/(?P<c>\d+)/$', views.dynamicData),
    url(r'^dynamicUpdate/$', views.dynamicUpdate, name = 'dynamicUpdate'),
    url(r'^analysis/$', views.analysis, name = 'analysis'),
    ]
