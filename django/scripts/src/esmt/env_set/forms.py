"""
Author: Yogaraja Gopal
This module takes care of Modeling Forms for Env Set App
"""
from django import forms


class EnvironmentSetForm(forms.Form):
    """
    This class is used to handle environment Set form
    """
    environment_set_name = forms.CharField(
        max_length=255, required=True,
        widget=forms.TextInput(attrs={'autocomplete': 'off', 'ng-cloak': 'True'}))

