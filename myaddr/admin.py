from django.contrib import admin

# Register your models here.
from .models import DwaAddr


class DwaAddrAdmin(admin.ModelAdmin):
    list_display = ('sortname', 'addr_name', 'phone1', 'email', 'postalcode')
    #	list_filter = ['lastname']
    search_fields = ['lastname']
    ordering = ['lastname']


admin.site.register(DwaAddr, DwaAddrAdmin)

admin.site.site_header = "David's Database"
admin.site.site_title = "David's site title"
admin.site.index_title = "David's main page"
