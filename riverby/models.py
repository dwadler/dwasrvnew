from django.db import models
from django.urls import reverse


# Create your models here.
class Address(models.Model):
    id = models.AutoField(primary_key=True)
    sort_name = models.CharField(max_length=32, blank=False)
    first_name = models.CharField(max_length=20, blank=True, default='', verbose_name='First Names')
    addr_name1 = models.CharField(max_length=32, blank=False, verbose_name='Address Name1')
    addr_name2 = models.CharField(max_length=32, blank=True, default='', verbose_name='Address Name2')
    addr_line1 = models.CharField(max_length=32, blank=False, verbose_name='Address Line1')
    addr_line2 = models.CharField(max_length=32, blank=True, verbose_name='Address Line2')
    city = models.CharField(max_length=40)
    state = models.CharField(max_length=40, blank=True, null=True)
    zip = models.CharField(max_length=20, blank=True, null=True)
    phone1 = models.CharField(max_length=30, blank=True, null=True)
    phone2 = models.CharField(max_length=30, blank=True, null=True)
    e_mail = models.CharField(max_length=64, blank=True, null=True, verbose_name='e-mail2')
    notes1 = models.CharField(max_length=128, blank=True, null=True)
    notes2 = models.CharField(max_length=128, blank=True, null=True)
    map_num = models.CharField(max_length=15, verbose_name='Map number')
    fire_num = models.IntegerField(verbose_name='Fire Number')
    rd_section = models.CharField(max_length=16, verbose_name='Road Name')
    purchase_date = models.CharField(max_length=10, blank=True, null=True)
    rhha = models.BooleanField()
    billable = models.BooleanField()
    archive = models.BooleanField()
    lastupdate = models.DateTimeField(blank=True, null=True, verbose_name='Last Update')
    updateby = models.CharField(max_length=20, blank=True, null=True, verbose_name='Updated By')

    def clone(self):
        new_kwargs = {fld.name: getattr(self, fld.name) for fld in self._meta.fields if fld.name != self._meta.pk}
        return self.__class__.objects.create(**new_kwargs)

    def __str__(self):
        return self.addr_name1

    def sortname(self):
        return self.sort_name

    def get_absolute_url(self):
        rv = reverse('riverby:address_list')
        print(f"\n*** in RbyAddresses::get_absolute_url -> {rv}")
        return rv

    sortname.admin_order_field = 'sort_name'
