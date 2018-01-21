from django.contrib.sitemaps import Sitemap
from .models import Hospital, Place


class PlaceSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.5

    def items(self):
        return Place.objects.all()

    def location(self, item):
        return item.get_absolute_url()


class HospitalSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Hospital.objects.all()

    def location(self, item):
        return item.get_absolute_url()
