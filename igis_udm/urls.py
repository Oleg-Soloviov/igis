from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^places/$', PlaceListView.as_view(), name='place_list'),
    url(r'^place/(?P<slug>\w+)/$', PlaceDetailView.as_view(), name='place'),
    url(r'^hospital/(?P<slug>[-\w]+)/$', HospitalDetailView.as_view(), name='hospital'),
    url(r'^login/$', HospitalLoginFormView.as_view(), name='login'),
    url(r'^logout/$', HospitalLogOutFormView.as_view(), name='logout'),
    url(r'^get_time/$', HospitalGetPersonTime.as_view(), name='get_time'),
    url(r'^signin/$', SignInFormView.as_view(), name='signin'),
    url(r'^signout/$', SignOutFormView.as_view(), name='signout'),
]