from django.db import models
from django.urls import reverse


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    address_type = models.CharField(max_length=1, verbose_name='Address Category')
    directorytype = models.CharField(max_length=1, verbose_name='Directory Category', default='m')
    advent = models.CharField(max_length=2, blank=True, null=True)
    envelopeno = models.IntegerField(blank=True, null=True, verbose_name='Envelope number')
    prefix = models.CharField(max_length=40, blank=True, null=True)
    lastname = models.CharField(max_length=40, blank=True, null=True, verbose_name='Last name')
    firstname = models.CharField(max_length=40, blank=True, null=True, verbose_name='First name')
    suffix = models.CharField(max_length=40, blank=True, null=True)
    addrline1 = models.CharField(max_length=40, blank=True, null=True, verbose_name='Address line1')
    addrline2 = models.CharField(max_length=40, blank=True, null=True, verbose_name='Address line2')
    city = models.CharField(max_length=40, blank=True, null=True)
    state = models.CharField(max_length=40, blank=True, null=True)
    country = models.CharField(max_length=40, blank=True, null=True)
    postalcode = models.CharField(max_length=20, blank=True, null=True, verbose_name='Zip')
    phone = models.CharField(max_length=32, blank=True, null=True)
    email = models.CharField(max_length=64, blank=True, null=True)
    family = models.CharField(max_length=40, blank=True, null=True)
    notes = models.CharField(max_length=1000, blank=True, null=True)
    cell1 = models.CharField(max_length=32, blank=True, null=True)
    cell2 = models.CharField(max_length=32, blank=True, null=True)
    archive = models.CharField(max_length=1, blank=True, null=True, default='N')
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    lastupdate = models.DateTimeField(blank=True, null=True, verbose_name='Last Update')
    updateby = models.CharField(max_length=20, blank=True, null=True, verbose_name='Updated by')

    def format_cell(self):
        content = f"{self.firstname} {self.lastname}\n"
        content += f"{self.addrline1}\n"
        if self.addrline2 is not None and len(self.addrline2) > 1:
            content += f"{self.addrline2}\n"
        content += f"{self.city}, {self.state} {self.postalcode}"
        if self.phone is not None and len(self.phone) > 0:
            content += f"\nphone: {self.phone}"
        if self.email is not None and len(self.email) > 0:
            content += f"\ne-mail: {self.email}"
        #        print ("\n ClcAddr::format_cell: content: {content}")
        return content

    def sortname(self):
        return self.lastname

    def get_absolute_url(self):
        rv = reverse('clc:address_list')
        return rv
