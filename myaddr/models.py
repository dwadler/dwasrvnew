from django.db import models
from django.urls import reverse


# Create your models here.


class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    service = models.CharField(max_length=32)
    name = models.CharField(max_length=40)
    notes = models.CharField(max_length=128, blank=True, null=True)
    lastupdate = models.DateTimeField(blank=True, null=True)
    updateby = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        print("*** in Movies::get_absolute_url *** try to get reverse\n")
        rv = reverse('myaddr:movie_list')
        print("*** reverse: '" + rv + "'\n")
        return rv


class DwaAddr(models.Model):
    id = models.AutoField(primary_key=True)
    xmas = models.CharField(max_length=1, blank=True, null=True)
    lastname = models.CharField(max_length=20, blank=True, null=True)
    addr_name = models.CharField(max_length=34, blank=True, null=True)
    addrline1 = models.CharField(max_length=40, blank=True, null=True)
    addrline2 = models.CharField(max_length=40, blank=True, null=True)
    city = models.CharField(max_length=40, blank=True, null=True)
    state = models.CharField(max_length=40, blank=True, null=True)
    country = models.CharField(max_length=40, blank=True, null=True)
    postalcode = models.CharField(max_length=20, blank=True, null=True)
    phone1 = models.CharField(max_length=32, blank=True, null=True)
    phone2 = models.CharField(max_length=32, blank=True, null=True)
    email = models.CharField(max_length=64, blank=True, null=True, verbose_name='e-mail')
    name1 = models.CharField(max_length=20, blank=True, null=True)
    name2 = models.CharField(max_length=20, blank=True, null=True)
    notes = models.CharField(max_length=128, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    lastupdate = models.DateTimeField(blank=True, null=True)
    updateby = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True, default='A')
    archive = models.CharField(max_length=1, blank=True, null=True, default='N')

    def __str__(self):
        return self.addr_name

    def sortname(self):
        return self.lastname

    def get_absolute_url(self):
        print("*** in get_absolute_url *** try to get reverse\n")
        rv = reverse('myaddr:myaddr_list')
        print("*** reverse: '" + rv + "'\n")
        return rv

    sortname.admin_order_field = 'lastname'
