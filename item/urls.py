from django.conf.urls import url

from item import views

urlpatterns = [
  url(r'^losts$', views.lostList),
  url(r'^lost/(?P<pk>[0-9]+)$', views.lostDetail),
  url(r'^lost/(?P<pk>[0-9]+)/complete$', views.completeLost),

  url(r'^founds$', views.foundList),
  url(r'^found/(?P<pk>[0-9]+)$', views.foundDetail),
  url(r'^found/(?P<pk>[0-9]+)/complete$', views.completeFound),
]
