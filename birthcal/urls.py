__author__ = 'chintanpanchamia'

from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    url(r'^accounts/login/$', views.login_view, name='login'),
    url(r'^accounts/logout/$', views.logout_view, name='logout'),
    url(r'^accounts/error/$', views.login_error_view, name='login_error'),
    url(r'^email/$', login_required(views.edit_email_view), name='custom_email'),
    url(r'^api/doctor/(?P<pk>[0-9]+)/$', login_required(views.DoctorView.as_view()), name='doctor'),
    url(r'^api/patient/(?P<pk>[0-9]+)/$', login_required(views.PatientView.as_view()), name='patient'),
    url(r'^oauth/$', views.oauth_view, name='oauth'),
    url(r'^$', login_required(views.index_view), name='index_view'),
]
