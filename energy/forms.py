from django.forms import CheckboxInput, ClearableFileInput, FileField
from django.forms import ModelForm, Form, CharField

from .models import EV6

YN_SELECT = [('Y', 'Y'), ('N', 'N')]


class EV6CreateForm(ModelForm):
    class Meta:
        model = EV6
        fields = [
            'date',
            'odometer',
            'new_miles', 'miles_per_kwh',
            'kwh', 'full_charge', 'location', 'notes',
            # Hidden fields
        ]
        widgets = {
            'full_charge': CheckboxInput(attrs={'class': 'required checkbox form-control'}),

        }


class MultipleFileInput(ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class UploadFileForm(Form):
    title = CharField(max_length=50)
    file = FileField()


class FileFieldForm(Form):
    file_field = MultipleFileField()
