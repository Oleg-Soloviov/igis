from django.urls import path, re_path
from .views import *
from django.contrib.sitemaps.views import sitemap
from .sitemaps import PlaceSitemap, HospitalSitemap

urlpatterns = [
    re_path(r'^hospital/(?P<slug>[-\w]+)/$', HospitalDetailView.as_view(), name='hospital'),
    path(r'login/', HospitalLoginFormView.as_view(), name='login'),
    path(r'logout/', HospitalLogOutFormView.as_view(), name='logout'),
    path(r'get_time/', HospitalGetPersonTime.as_view(), name='get_time'),
    path(r'signin/', SignInFormView.as_view(), name='signin'),
    path(r'signout/', SignOutFormView.as_view(), name='signout'),
    path('sitemap.xml', sitemap, {'sitemaps': {'Place': PlaceSitemap, 'Hospital': HospitalSitemap}},
         name='django.contrib.sitemaps.views.sitemap'),
    path(r'contacts/', ContactView.as_view(), name='contacts'),
    path(r'contacts/success/', ContactSuccessView.as_view(), name='contacts_success'),
    re_path(r'^(?P<slug>\w+)/$', PlaceDetailView.as_view(), name='place'),
    re_path(r'^$', PlaceListView.as_view(), name='place_list'),
]
