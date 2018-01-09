from django.contrib import admin
from .models import Place, Hospital, DayofWeek, Person, Speciality

admin.site.register(Place)
admin.site.register(Hospital)
admin.site.register(Person)
admin.site.register(Speciality)

