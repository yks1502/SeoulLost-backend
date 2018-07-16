from django.conf.urls import url

from item import views

urlpatterns = [
  url(r'^losts$', views.lostlist),
  url(r'^lost/(?P<pk>[0-9]+)$', views.lostDetail),
  url(r'^lost/(?P<pk>[0-9]+)/complete$', views.complete_lost),

  url(r'^founds$', views.foundlist),
  url(r'^found/(?P<pk>[0-9]+)$', views.foundDetail),
  url(r'^found/(?P<pk>[0-9]+)/complete$', views.complete_found),
]
