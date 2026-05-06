from django.contrib import admin

# Register your models here.
from .models import Address


class AddressAdmin(admin.ModelAdmin):
    list_display = ('lastname', 'firstname', 'phone', 'email', 'postalcode')
    #	list_filter = ['lastname']
    search_fields = ['lastname']
    ordering = ['lastname']


admin.site.register(Address)

admin.site.site_header = "CLC Database"
admin.site.site_title = "CLC site title"
admin.site.index_title = "CLC main page"
