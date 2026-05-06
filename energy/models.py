from django.db import models
from django.urls import reverse


# Create your models here.
class Electrical(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(max_length=10, blank=False, null=False)
    kwh = models.IntegerField()
    meter_reading = models.IntegerField()
    solar_balance = models.IntegerField()
    ch_base = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    ch_delivery = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    ch_supply = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    ch_prev = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    ch_curr = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    ch_adjustment = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    ch_total = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    ch_bill = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    lastupdate = models.DateTimeField(blank=True, null=True)
    notes = models.CharField(max_length=32, blank=True, null=True)
    updateby = models.CharField(max_length=20, blank=True, null=True)

    def get_absolute_url(self):
        rv = reverse('energy:electrical_list')
        return rv

    def __str__(self):
        list_representation = (f"id: {self.id}; date: {self.date}; kwh: {self.kwh}; cost: {self.ch_total}")
        #        print (f"Electrical:: __str__ {list_representation}")
        return list_representation


class EV6(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(max_length=10, blank=False, null=False)
    odometer = models.IntegerField()
    new_miles = models.IntegerField()
    miles_per_kwh = models.DecimalField(decimal_places=1, max_digits=5, blank=True, null=True, default=0)
    kwh = models.DecimalField(decimal_places=1, max_digits=5, blank=True, null=True)
    mkwh = models.DecimalField(decimal_places=1, max_digits=5, blank=True, null=True, default=0)
    full_charge = models.BooleanField()
    location = models.CharField(max_length=20, blank=True, null=True)
    notes = models.CharField(max_length=64, blank=True, null=True)

    def get_absolute_url(self):
        rv = reverse('energy:ev6_list')
        return rv

    def __str__(self):
        list_representation = (f"id: {self.id}; date: {self.date}; cost: {self.odometer};"
                               f" cost: {self.new_miles}; kwh: {self.kwh}; full_charge: {self.full_charge}")
        return list_representation


class EnergyData(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(max_length=10, blank=False, null=False)

    solar_kwh = models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True, default=0)
    max_kwh = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    main_a = models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True, default=0)
    main_b = models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True, default=0)
    main_total = models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True, default=0)
    mini_split = models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True, default=0)

    garage_a = models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True, default=0)
    garage_b = models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True, default=0)
    garage_total = models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True, default=0)
    solar = models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True, default=0)
    ev = models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True, default=0)

    def get_absolute_url(self):
        rv = reverse('energy:ev6_list')
        return rv

    def __str__(self):
        list_representation = (f"id: {self.id}; date: {self.date}")
        return list_representation
