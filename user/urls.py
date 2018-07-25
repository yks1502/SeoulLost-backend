from django.conf.urls import url

from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
  url(r'signup$', views.userSignup),
  url(r'login$', obtain_auth_token),
  url(r'profile$', views.get_user),
  url(r'^userlist$', views.UserList.as_view()),
  url(r'duplicate$', views.duplicateUsername),
  url(r'items$', views.userItems),
  url(r'alarms$', views.userAlarms)
]
