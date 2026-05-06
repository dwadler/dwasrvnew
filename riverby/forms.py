from django.forms import ModelForm, CharField
from django.forms import RadioSelect
from django.forms import TextInput, IntegerField, ChoiceField, Textarea, HiddenInput

from riverby.models import Address

RHHA_ROAD_CHOICES = [
    ("Abbey Road", "Abbey Road"),
    ("Erika's Walk", "Erika's Walk"),
    ("Jim's Road", "Jim's Road"),
    ("Middle Way", "Middle Way"),
    ("The High Road", "The High Road"),
    ("Velvet Underpass", "Velvet Underpass"),
    ("Other", "Other"),
]
YN_SELECT = [(True, 'Y'), (False, 'N')]


class RiverbyCreateForm(ModelForm):
    old_id = IntegerField(initial=0, widget=HiddenInput())
    rd_section = ChoiceField(choices=RHHA_ROAD_CHOICES, label='Road')
    e_mail = CharField(widget=TextInput(attrs={'size': '50'}))

    class Meta:
        model = Address
        fields = [
            'map_num', 'fire_num', 'rd_section',
            'sort_name', 'first_name', 'addr_name1', 'addr_name2',
            'addr_line1', 'addr_line2', 'city', 'state', 'zip', 'phone1',
            'phone2', 'e_mail', 'purchase_date', 'notes1', 'notes2',
            'archive',
            'rhha', 'billable',
            # Hidden fields
        ]
        widgets = {
            'notes2': Textarea(attrs={'rows': 2, 'cols': 60}),
            'archive': RadioSelect(choices=YN_SELECT),
            'rhha': RadioSelect(choices=YN_SELECT),
            'billable': RadioSelect(choices=YN_SELECT),
        }
        labels = {
            'rhha': 'RHHA',
        }


class RiverbyUpdateForm(ModelForm):
    old_id = IntegerField(initial=0, widget=HiddenInput())
    e_mail = CharField(widget=TextInput(attrs={'size': '50'}))
    updateby = CharField(disabled=True, label='Updated By', required=False)
    lastupdate = CharField(disabled=True, label='Last Update', required=False)
    rd_section = ChoiceField(choices=RHHA_ROAD_CHOICES, label='Road')

    class Meta:
        model = Address

        fields = [
            'map_num', 'fire_num', 'rd_section',
            'sort_name', 'first_name', 'addr_name1', 'addr_name2',
            'addr_line1', 'addr_line2', 'city', 'state', 'zip', 'phone1',
            'phone2', 'e_mail', 'purchase_date', 'notes1', 'notes2',
            'archive',
            'rhha', 'billable',
            'lastupdate', 'updateby',
            # Hidden fields
        ]
        widgets = {
            'notes1': Textarea(attrs={'rows': 2, 'cols': 60}),
            'notes2': Textarea(attrs={'rows': 2, 'cols': 60}),
            'archive': RadioSelect(choices=YN_SELECT),
            'rhha': RadioSelect(choices=YN_SELECT),
            'billable': RadioSelect(choices=YN_SELECT),
        }
        labels = {
            'rhha': 'RHHA',
        }
