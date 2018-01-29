from django.contrib import admin
from .models import Place, Hospital, Person, Speciality, SEOitems


class HospitalAdmin(admin.ModelAdmin):
    search_fields = ['id', 'name']


admin.site.register(Place)
admin.site.register(Hospital, HospitalAdmin)
admin.site.register(Person)
admin.site.register(Speciality)
admin.site.register(SEOitems)
