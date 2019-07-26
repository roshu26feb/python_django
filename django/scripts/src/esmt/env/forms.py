"""
Author: Yogaraja Gopal
This module takes care of Modeling Forms for Env App
"""
from django import forms
from esmt.api.mixins import CreationDateMixin
from esmt.api.choice_list import EnvDataType


class EnvironmentForm(CreationDateMixin, forms.Form):
    """
    This class is used to handle environment form
    """
    environment_name = forms.CharField(
        max_length=255, required=True,
        widget=forms.TextInput(
            attrs={'autocomplete': 'off', 'ng-cloak': 'True',
                   'value': '(~envType.environment_type_short_name~)_(~sys.system_short_name~)'
                            '_(~inc~)_(~suffix~)', 'readonly': 'readonly'}))
    inc_number = forms.CharField(max_length=3, required=True, label='ID',
                                 help_text='Valid value (001-999)',
                                 widget=forms.TextInput(
                                     attrs={'autocomplete': 'off', 'pattern': '^\d{3}$',
                                            'ng-model': 'inc'}))
    suffix = forms.CharField(max_length=7, required=True,
                             help_text='Example: Socrates = SOC3UK (max 7 characters)',
                             widget=forms.TextInput(
                                 attrs={'autocomplete': 'off', 'ng-model': 'suffix',
                                        'pattern': '[a-zA-Z0-9]{1,7}'}))

    def __init__(self,request, *args, **kwargs):
        super(EnvironmentForm, self).__init__(*args, **kwargs)

        self.fields['environment_data_type'] = forms.ChoiceField(
            choices=EnvDataType(request.COOKIES['access_token']).get_choices(),
            widget=forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true'}))

        self.order_fields(['environment_type', 'inc_number', 'suffix', 'environment_name',
                           'environment_data_type'])
