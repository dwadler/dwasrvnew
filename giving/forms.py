from django.forms import HiddenInput, DateField
from django.forms import IntegerField, DecimalField, TextInput
from django.forms import ModelForm, SelectDateWidget, CharField, RadioSelect

from .models import Donor, Donation

YN_SELECT = [('Y', 'Y'), ('N', 'N')]
YEAR_CHOICES = ["2023", "2024", "2025", "2026"]


class DonorForm(ModelForm):
    model = Donor
    YN_SELECT = [('Y', 'Y'), ('N', 'N')]
    first_name = CharField(required=False, max_length=64)
    last_name = CharField(required=True, max_length=64)
    envelopeno = IntegerField()
    notes = CharField(required=False)
    active = CharField(required=True, label='Active', widget=RadioSelect(choices=YN_SELECT))

    class Meta:
        model = Donor
        fields = ['prefix', 'first_name', 'last_name', 'envelopeno', 'addr1', 'addr2', 'city',
                  'state', 'zip',
                  'email', 'lastupdate',
                  'notes',
                  'updateby', 'active',
                  ]


class DonationForm(ModelForm):
    model = Donation

    donor_id = IntegerField(required=False,widget=HiddenInput())
    processed_date = DateField(widget=SelectDateWidget(years=YEAR_CHOICES))
    amount = DecimalField(widget=TextInput(attrs={'autofocus': True}))
    special_amount = DecimalField(required=False)
    occasion = CharField(required=False, max_length=32)

    class Meta:
        model = Donation
        fields = ['donor_id', 'processed_date', 'amount', 'special_amount', 'occasion'
                  ]
