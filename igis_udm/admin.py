from django.contrib import admin
from .models import Place, Hospital, Person, Speciality, SEOitems

admin.site.register(Place)
admin.site.register(Hospital)
admin.site.register(Person)
admin.site.register(Speciality)
admin.site.register(SEOitems)

