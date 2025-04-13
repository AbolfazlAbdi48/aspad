from django import forms
from .models import Gym, GymSession


class GymForm(forms.ModelForm):
    class Meta:
        model = Gym
        fields = '__all__'
        exclude = ('owner',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.DateTimeInput):
                field.widget.attrs['class'] = 'form-control'


class GymSessionForm(forms.ModelForm):
    class Meta:
        model = GymSession
        fields = '__all__'
        exclude = ('gym', 'reserved_by')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.DateTimeInput):
                field.widget.attrs['class'] = 'form-control'
