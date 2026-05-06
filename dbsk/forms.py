from django.forms import HiddenInput, Form, DateInput, BooleanField
from django.forms import IntegerField, DecimalField, TextInput, Textarea
from django.forms import ModelForm, DateField, ModelChoiceField, CharField, RadioSelect

from home.dwaforms import DwaBaseForm
from .models import Schedule, Volunteer, Provider
from .models_donor import Donor, Donation

YN_SELECT = [('Y', 'Y'), ('N', 'N')]
CONTACT_CHOICES = (('P', 'Phone'),
                   ('E', 'e-mail'),
                   ('T', 'Text'))


class MyDateInput(DateInput):
    input_type = 'date'


class VolunteerReportForm(Form):
    startDate = DateField(label='Start date:', widget=MyDateInput)
    endDate = DateField(label='End date:', widget=MyDateInput)


class SMSAllowForm(Form):
    name = CharField(max_length=50, label='Name')
    phoneNumber = CharField(max_length=20, label='Phone')
    smsAllow = BooleanField()


class MessageInputForm(Form):
    subject = CharField(max_length=50, label='Subject')
    messageText = CharField(max_length=1000, label='Message text', widget=Textarea(attrs={'rows': 10, 'cols': 60}))


class VolunteerCreateForm(ModelForm):
    class Meta:
        model = Volunteer
        exclude = ['updateby', 'lastupdate']
        fields = '__all__'
        widgets = {
            'preferred_contact': RadioSelect(choices=CONTACT_CHOICES),
            'archive': RadioSelect(choices=YN_SELECT),
            'notes': Textarea(attrs={'rows': 2, 'cols': 60}),
        }


class VolunteerUpdateForm(DwaBaseForm):
    # updateby and lastupdate disabled by DwaBaseForm
    class Meta:
        model = Volunteer
        fields = '__all__'
        widgets = {
            'preferred_contact': RadioSelect(choices=CONTACT_CHOICES),
            'archive': RadioSelect(choices=YN_SELECT),
            'notes': Textarea(attrs={'rows': 2, 'cols': 60}),
        }


class ProviderCreateForm(ModelForm):
    class Meta:
        model = Provider
        exclude = ['updateby', 'lastupdate']
        fields = '__all__'
        widgets = {
            'archive': RadioSelect(choices=YN_SELECT),
            'notes': Textarea(attrs={'rows': 2, 'cols': 60}),
        }


class ProviderUpdateForm(DwaBaseForm):
    # updateby and lastupdate disabled by DwaBaseForm
    class Meta:
        model = Provider
        fields = '__all__'
        widgets = {
            'archive': RadioSelect(choices=YN_SELECT),
            'notes': Textarea(attrs={'rows': 2, 'cols': 60}),
        }


class ScheduleForm(ModelForm):
    model = Schedule
    schedule_date = DateField(widget=HiddenInput())
    volunteers = Volunteer.objects.all().exclude(archive='Y')
    volunteer1 = ModelChoiceField(queryset=volunteers)
    volunteer2 = ModelChoiceField(queryset=volunteers)
    providers = Provider.objects.all().exclude(archive='Y')
    provider = ModelChoiceField(queryset=providers)
    notes = CharField(required=False)

    class Meta:
        model = Schedule
        fields = ['schedule_date', 'provider', 'volunteer1', 'volunteer2', 'notes']


class DonorForm(ModelForm):
    model = Donor
    YN_SELECT = [('Y', 'Y'), ('N', 'N')]
    first_name = CharField(required=False, max_length=64)
    last_name = CharField(required=True, max_length=64)
    notes = CharField(required=False)
    active = CharField(required=True, label='Active', widget=RadioSelect(choices=YN_SELECT))

    class Meta:
        model = Donor
        fields = ['prefix', 'first_name', 'last_name', 'addr1', 'addr2', 'city',
                  'state', 'zip',
                  'email', 'lastupdate',
                  'notes',
                  'updateby', 'active',
                  ]


class DonationForm(ModelForm):
    model = Donation

    donor_id = IntegerField(widget=HiddenInput())
    amount = DecimalField(widget=TextInput(attrs={'autofocus': True}))
    check_no = CharField(max_length=16)
    check_date = DateField()
    occasion = CharField(required=False, max_length=32)

    class Meta:
        model = Donation
        fields = ['amount', 'check_no', 'check_date', 'occasion', 'donor_id'
                  ]
