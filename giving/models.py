from django.db import models
from django.urls import reverse


class Donor(models.Model):
    id = models.AutoField(primary_key=True)
    envelopeno = models.IntegerField(blank=True, null=True, verbose_name='Envelope number')
    clc_addr_id = models.IntegerField(blank=True, null=True)
    prefix = models.CharField(max_length=10, blank=True, null=True)
    first_name = models.CharField(max_length=64, blank=True, null=True)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    addr1 = models.CharField(max_length=32, blank=True, null=True)
    addr2 = models.CharField(max_length=32, blank=True, null=True)
    city = models.CharField(max_length=32, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    zip = models.CharField(max_length=10, blank=True, null=True)
    email = models.CharField(max_length=64, blank=True, null=True)
    lastupdate = models.DateTimeField(blank=True, null=True)
    notes = models.CharField(max_length=64, blank=True, null=True)
    updateby = models.CharField(max_length=20, blank=True, null=True)
    active = models.CharField(max_length=1, blank=True, null=True, default='Y')

    def get_absolute_url(self):
        rv = reverse('giving:donor_list')
        return rv

    def __str__(self):
        list_representation = ("%s %s"
                               % (self.first_name
                                      , self.last_name))
        #        print (list_representation)
        return list_representation


class Donation(models.Model):
    id = models.AutoField(primary_key=True)
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    #    donor_id = models.IntegerField(blank=True, null=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    special_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    occasion = models.CharField(max_length=32, blank=True, null=True)
    processed_date = models.DateTimeField(max_length=32, blank=True, null=True)
    batch = models.IntegerField(blank=True, null=True)
    lastupdate = models.DateTimeField(max_length=32, blank=True, null=True)
    updateby = models.CharField(max_length=20, blank=True, null=True)

    def get_absolute_url(self):
        rv = reverse('giving:donate_list')
        return rv

    def __str__(self):
        list_representation = ("Date: %s Amount: %s Special amount: %s Occasion: %s"
                               % (
                                   self.processed_date
                                   , self.amount
                                   , self.special_amount
                                   , self.occasion
                               )
                               )
        #        print (list_representation)
        return list_representation
