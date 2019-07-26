"""
Author: Yogaraja Gopal
Date : 12-04-2018
This module contains the forms used for Esmt Admin
"""
from django import forms
from esmt.api.choice_list import ParameterType, UserRole, Users


class ReferenceDataForm(forms.Form):
    """
    This class is used to handle Reference Data form
    """
    DATA_CHOICE = [("", "--Select--"),
                   ("host_type", "Host Type"), ("infrastructure_type", "Infrastructure Type"),
                   ("disk_type", "Disk Type"), ("method_creation_type", "Method Creation Type"),
                   ("component_type", "Component Type"), ("deployment_type", "Deployment Type"),
                   ("artefact_type", "Artefact Type"), ("environment_type", "Environment Type"),
                   ("environment_subscription_type", "Environment Subscription Type"),
                   ("environment_data_type", "Environment Data Type"), ("status", "Status"),
                   ("parameter_type", "Parameter Type"), ("environment_use", "Environment Use"), ("system_network_set", "System Network Set"), ("system_element_type", "System Element Type"),
                   ("host_region", "Host Region Type"), ("host_site", "Host Site Type"), ("host_subscription", "Host Subscriptions"), ("network_set", "Network Set")]
    data = forms.ChoiceField(
        choices=DATA_CHOICE, widget=forms.Select(
            attrs={'class': 'form-control selectpicker', 'data-live-search': 'true',
                   'ng-model': 'ref_data',
                   'ng-change': 'getApiDetails(ref_data); refDataTableHead(ref_data)'}))


class ParameterForm(forms.Form):
    """
    This class is used to handle parameter form
    """
    TRUE_FALSE = [('', '--Select--'), ('true', 'True'), ('false', 'False')]
    LINK_CHOICES = [('component_type_id', 'Component Type'), ('component_id', 'Component'),
                    ('component_version_id', 'Component Version')]
    parameter_name = forms.CharField(
        max_length=255, required=True, label='Parameter Display Name',
        widget=forms.TextInput(attrs={'autocomplete': 'off', 'class': 'form-control',
                                      'ng-model': 'p.paramDispName'}))
    parameter_internal_name = forms.CharField(
        max_length=255, required=True, label='Parameter Name',
        help_text="Key enclosed in single ' and values separated by . character are allowed eg 'Infrastructure'.'Azure'",
        widget=forms.TextInput(attrs={'autocomplete': 'off', 'class': 'form-control',
                                      'ng-model': 'p.paramInternalName','pattern': "^[A-Za-z0-9_'.:]+$"}))
    parameter_type_name = forms.CharField(
        max_length=255, required=False, widget=forms.HiddenInput(
            attrs={'ng-model': 'p.paramTypeName'}))
    mandatory = forms.ChoiceField(
        choices=TRUE_FALSE, required=True, widget=forms.Select(attrs={'class': 'form-control',
                                                                      'ng-model': 'p.mandatory'}))
    active = forms.ChoiceField(
        choices=TRUE_FALSE, required=True,
        widget=forms.Select(attrs={'class': 'form-control', 'ng-model': 'p.active'}))
    # link = forms.ChoiceField(required=False, choices=LINK_CHOICES,
    #                          widget=forms.Select(
    #                              attrs={'autocomplete': 'off', 'ng-model': 'p.link',
    #                                     'ng-change': 'getLinkedItemsChoice(p.link)'}))

    def __init__(self, *args, **kwargs):
        if kwargs:
            request = kwargs.pop("request")
        else:
            request = args[0]["request"]
        super(ParameterForm, self).__init__(*args, **kwargs)
        self.fields['parameter_type'] = forms.ChoiceField(
            choices=ParameterType(request.COOKIES['access_token']).get_choices(),
            widget=forms.Select(attrs={'class': 'form-control', 'ng-model': 'p.paramType',
                                       'ng-change': 'addParameterValues(p.paramType)'}))
        self.order_fields(['parameter_name', 'mandatory'])


class AddUserForm(forms.Form):
    """
    This class is used to handle Add User form
    """
    display_name = forms.CharField(max_length=255, required=True,
                                   widget=forms.TextInput(
                                       attrs={'autocomplete': 'off', 'class': 'form-control'}))
    user_name = forms.RegexField(max_length=255, required=True, regex='^[\w.]+$',
                                 help_text='Please enter as firstname.lastname',
                                 widget=forms.TextInput(
                                     attrs={'autocomplete': 'off', 'class': 'form-control',
                                            'pattern': '^[\w.]+$'}))
    email_address = forms.EmailField(max_length=255, required=True,
                                     widget=forms.EmailInput(
                                         attrs={'autocomplete': 'off', 'class': 'form-control'}))


class UserRoleForm(forms.Form):
    """
    This class is used to handle User Role form
    """
    email = forms.CharField(max_length=255, required=True,
                            widget=forms.TextInput(
                                attrs={'autocomplete': 'off', 'class': 'form-control',
                                       'readonly': 'readonly', 'ng-model': 'users.email_address'}))

    def __init__(self, request, user_id, *args, **kwargs):
        super(UserRoleForm, self).__init__(*args, **kwargs)
        self.user_id = user_id
        self.fields['user'] = forms.ChoiceField(
            choices=Users(request.COOKIES['access_token']).get_choices(),
            widget=forms.Select(
                attrs={'class': 'form-control selectpicker', 'data-live-search': 'true',
                       'ng-model': 'user', 'ng-change': 'getUserById(user)',
                       'ng-init': "user='" + str(self.user_id) + "';getUserById(user)"}))
        self.fields['user_roles'] = forms.MultipleChoiceField(choices=UserRole(request.COOKIES['access_token']).get_choices(),
                                                              widget=forms.CheckboxSelectMultiple)
        self.order_fields(['user', 'email'])
