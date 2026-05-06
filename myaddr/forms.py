from django.forms import ModelForm, CharField
from django.forms import RadioSelect
from django.forms import TextInput, ChoiceField, Textarea

from .models import DwaAddr, Movie

YN_SELECT = [('Y', 'Y'), ('N', 'N')]

SERVICES = [
    ('Netflix', 'Netflix'),
    ('Amazon Prime', 'Amazon Prime'),
    ('Hulu', 'Hulu'),
    ('HBO', 'HBO'),
    ('Apple+', 'Apple+'),
    ('Peacock', 'Peacock'),
    ('Other', 'Other')
]


class MovieCreateForm(ModelForm):
    service = ChoiceField(choices=SERVICES)

    class Meta:
        model = Movie
        fields = [
            'service',
            'name',
            'notes',
        ]


class MovieUpdateForm(ModelForm):
    service = ChoiceField(choices=SERVICES)

    class Meta:
        model = Movie
        fields = [
            'date',
            'service',
            'name',
            'notes',
        ]


class AddressCreateForm(ModelForm):
    class Meta:
        model = DwaAddr
        fields = [
            'status',
            'xmas',
            'lastname', 'addr_name', 'addrline1', 'addrline2',
            'city', 'state', 'postalcode', 'country', 'phone1',
            'phone2', 'email', 'name1', 'name2', 'notes', 'latitude', 'longitude',
            'archive',

        ]
        widgets = {
            'notes1': Textarea(attrs={'rows': 2, 'cols': 60}),
            'archive': RadioSelect(choices=YN_SELECT),
            'xmas': RadioSelect(choices=YN_SELECT),
            'status': RadioSelect(choices=YN_SELECT),
        }


class AddressUpdateForm(ModelForm):
    updateby = CharField(disabled=True, label='Updated By', required=False)
    lastupdate = CharField(disabled=True, label='Last Update', required=False)

    class Meta:
        model = DwaAddr
        fields = [
            'status',
            'xmas',
            'lastname', 'addr_name', 'addrline1', 'addrline2',
            'city', 'state', 'postalcode', 'country', 'phone1',
            'phone2', 'email', 'name1', 'name2', 'notes', 'latitude', 'longitude',
            'archive',
            'lastupdate', 'updateby',

        ]
        widgets = {
            'notes1': Textarea(attrs={'rows': 2, 'cols': 60}),
            'archive': RadioSelect(choices=YN_SELECT),
            'xmas': RadioSelect(choices=YN_SELECT),
            'status': RadioSelect(choices=YN_SELECT),
            'addr_name': TextInput(attrs={'autofocus': True})
        }
