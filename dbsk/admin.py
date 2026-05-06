from django.contrib import admin

# Register your models here.
from .models import Volunteer, Schedule, Provider


class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('lastname', 'firstname', 'phone1', 'phone2', 'email', 'availability', 'notes')
    #	list_filter = ['lastname']
    search_fields = ['lastname']
    ordering = ['lastname']
    fields = ('lastname', 'firstname', 'phone1', 'phone2', 'email', 'availability', 'notes')


class ScheduleAdmin(admin.ModelAdmin):
    ordering = ['schedule_date']


#	fields = ('schedule_date', 'preferred_day')

class ProviderAdmin(admin.ModelAdmin):
    ordering = ['provider_name']
    fields = ('provider_name', 'addr1', 'addr2', 'city', 'state', 'zip', 'status', 'phone1')
    list_display = ('provider_name', 'status', 'phone1', 'notes')


admin.site.register(Volunteer, VolunteerAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Provider, ProviderAdmin)
