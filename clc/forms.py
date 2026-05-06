from django.forms import ChoiceField
from django.forms import ModelForm, RadioSelect
from django.forms import TextInput, Textarea

from .models import Address

YN_SELECT = [('Y', 'Y'), ('N', 'N')]
ADDRESS_TYPE_CHOICES = [
    ("f", "Friend"),
    ("m", "Member"),
    ("c", "Church"),
    ("i", "Inactive"),
    ("x", "Other"),
    ("d", "Deceased"),
    ("e", "E"),
]
DIRECTORY_TYPE_CHOICES = [
    ("d", "Church Directory"),
    ("f", "Friend"),
    ("c", "Church"),
    ("i", "Inactive"),
    ("x", "Other"),
]
ADVENT_TYPE_CHOICES = [
    ("N", "N"),
    ("C", "C"),
    ("I", "I"),
    ("X", "Exclude"),
]

class ListByTypeForm(ModelForm):
    address_type = ChoiceField(choices=ADDRESS_TYPE_CHOICES)
    print(f"ListByType:: address_type: {address_type}")

    class Meta:
        model = Address
        fields = ['address_type']


class AddressCreateForm(ModelForm):
    address_type = ChoiceField(choices=ADDRESS_TYPE_CHOICES, label='Address Type')
    directorytype = ChoiceField(choices=DIRECTORY_TYPE_CHOICES, label='Directory Type')
    advent = ChoiceField(choices=ADVENT_TYPE_CHOICES, label='Advent')

    class Meta:
        model = Address
        fields = ['firstname', 'lastname',
                  'addrline1', 'addrline2', 'city', 'state', 'postalcode',
                  'email', 'phone', 'cell1', 'cell2', 'notes',
                  'advent', 'address_type', 'directorytype', 'archive',
                  ]
        widgets = {
            'archive': RadioSelect(choices=YN_SELECT),
            'notes': Textarea(attrs={'rows': 2, 'cols': 60}),
            'email': Textarea(attrs={'rows': 2, 'cols': 32}),
        }


class AddressUpdateForm(ModelForm):
    address_type = ChoiceField(choices=ADDRESS_TYPE_CHOICES, label='Address Type')
    directorytype = ChoiceField(choices=DIRECTORY_TYPE_CHOICES, label='Directory Type')
    advent = ChoiceField(choices=ADVENT_TYPE_CHOICES, label='Advent')

    class Meta:
        model = Address
        fields = ['envelopeno', 'firstname', 'lastname',
                  'addrline1', 'addrline2', 'city', 'state', 'postalcode',
                  'email', 'phone', 'cell1', 'cell2', 'notes',
                  'advent', 'address_type', 'directorytype',
                  'archive', 'updateby', 'lastupdate',
                  'latitude', 'longitude',
                  ]
        widgets = {
            'archive': RadioSelect(choices=YN_SELECT),
            'notes': Textarea(attrs={'rows': 2, 'cols': 60}),
            'email': Textarea(attrs={'rows': 2, 'cols': 32}),
            'postalcode': TextInput(attrs={'size': 10})
        }
