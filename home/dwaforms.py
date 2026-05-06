from django.forms import ModelForm, CharField

YN_SELECT = [('Y', 'Y'), ('N', 'N')]


class DwaBaseForm(ModelForm):
    updateby = CharField(required=False, disabled=True, label='Updated By')
    lastupdate = CharField(required=False, disabled=True, label='Last Update')
