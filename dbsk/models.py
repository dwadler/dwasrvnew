import calendar

from django.db import models
from django.urls import reverse


class Volunteer(models.Model):
    firstname = models.CharField(max_length=20, blank=False, null=False, verbose_name='First name')
    lastname = models.CharField(max_length=20, blank=False, null=False, verbose_name='Last name')
    addr1 = models.CharField(max_length=40, blank=True, null=True, verbose_name='Address line 1')
    addr2 = models.CharField(max_length=40, blank=True, null=True, verbose_name='Address line 2')
    city = models.CharField(max_length=40, blank=True, null=True)
    state = models.CharField(max_length=20, blank=True, null=True)
    zip = models.CharField(max_length=10, blank=True, null=True)
    phone1 = models.CharField(max_length=32, blank=False, null=False, default='None')
    phone2 = models.CharField(max_length=32, blank=True, null=True)
    email = models.CharField(max_length=32, blank=True, null=True)
    preferred_contact = models.CharField(max_length=1, blank=True, null=True, default='P')
    notes = models.CharField(max_length=120, blank=True, null=True)
    availability = models.CharField(max_length=16, blank=True, null=True)
    lastupdate = models.DateTimeField(blank=True, null=True)
    updateby = models.CharField(max_length=20, blank=True, null=True)
    archive = models.CharField(max_length=1, default='N')

    class Meta:
        ordering = ('archive', 'lastname')

    def __str__(self):
        return self.firstname + " " + self.lastname + " - " + self.phone1

    def get_absolute_url(self):
        rv = reverse('dbsk:volunteer_list')
        print(f"*** Volunteer:get_absolute_url *** reverse URL: {rv}")
        return rv


class Provider(models.Model):
    provider_name = models.CharField(max_length=32, blank=False, null=False)
    contact_name = models.CharField(max_length=20, blank=True, null=True)
    preferred_day = models.CharField(max_length=20, blank=True, null=True)
    addr1 = models.CharField(max_length=40, blank=True, null=True, verbose_name='Address line 1')
    addr2 = models.CharField(max_length=40, blank=True, null=True, verbose_name='Address line 2')
    city = models.CharField(max_length=40, blank=True, null=True)
    state = models.CharField(max_length=20, blank=True, null=True)
    zip = models.CharField(max_length=10, blank=True, null=True)
    phone1 = models.CharField(max_length=32, blank=False, null=False, default='None')
    phone2 = models.CharField(max_length=32, blank=True, null=True)
    email = models.CharField(max_length=32, blank=True, null=True)
    notes = models.CharField(max_length=120, blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)
    lastupdate = models.DateTimeField(blank=True, null=True)
    updateby = models.CharField(max_length=20, blank=True, null=True)
    archive = models.CharField(max_length=1, default='N')

    class Meta:
        ordering = ('archive', 'provider_name')

    def __str__(self):
        return self.provider_name + " - " + self.phone1

    def get_absolute_url(self):
        rv = reverse('dbsk:provider')
        print(f"*** Provider:get_absolute_url *** reverse URL: {rv}")
        return rv


class Schedule(models.Model):
    schedule_date = models.DateField('date scheduled')
    volunteer1 = models.ForeignKey(Volunteer, on_delete=models.PROTECT, related_name='volunteer1')
    volunteer2 = models.ForeignKey(Volunteer, on_delete=models.PROTECT, related_name='volunteer2')
    provider = models.ForeignKey(Provider, on_delete=models.PROTECT, related_name='provider')
    s_year = models.IntegerField(blank=True, null=True)
    s_month = models.IntegerField(blank=True, null=True)
    s_day = models.IntegerField(blank=True, null=True)
    notes = models.CharField(max_length=40, null=True)
    lastupdate = models.DateTimeField(blank=True, null=True)
    updateby = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        day = calendar.day_name[self.schedule_date.weekday()]
        list_representation = ("%s(%s) : %s : %s : %s" \
                               % (self.schedule_date.isoformat()
                                      , day
                                      , self.provider.provider_name
                                      , self.volunteer1
                                      , self.volunteer2))
        #        print (list_representation)
        return list_representation

    def get_absolute_url(self):
        rv = reverse('dbsk:schedule')
        print(f"*** Schedule:get_absolute_url *** reverse URL: {rv}")
        return rv
