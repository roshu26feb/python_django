"""
Author: Yogaraja Gopal
This module contains the forms used delivery_db app
"""
from django import forms
from esmt.api.choice_list import Components, ComponentType, Systems, SystemNetworkSet, \
    ArtefactStoreType, HostType, DeploymentType, InfraTemplate, MethodCreation, InfraType, HostRegion
from esmt.api.mixins import CreationDateMixin
import requests


class SystemForm(CreationDateMixin, forms.Form):
    """
    This class is used to handle System form
    """
    system_name = forms.CharField(max_length=255, required=True,
                                  widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    system_short_name = forms.CharField(max_length=255, required=True,
                                        widget=forms.TextInput(attrs={'autocomplete': 'off'}))

    def __init__(self,request, *args, **kwargs):
        super(SystemForm, self).__init__(*args, **kwargs)
        self.fields['system_network_set_id'] = forms.ChoiceField(
            label="System Network Set",
            choices=SystemNetworkSet(request.COOKIES['access_token']).get_choices(),
            widget=forms.Select(attrs={'autocomplete': 'off'}))
        self.order_fields(['system_name'])


class SystemVersionForm(CreationDateMixin, forms.Form):
    """
    This class is used to handle System Version  form
    """
    system_version_name = forms.CharField(max_length=255, required=True,
                                          widget=forms.TextInput(attrs={'autocomplete': 'off'}))

    def __init__(self,request, *args, **kwargs):
        # print(self.request)
        super(SystemVersionForm, self).__init__(*args, **kwargs)
        # print(requests.Session())
        # session = requests.Session()
        # print(session.cookies.get_dict())
        self.fields['system_name'] = forms.ChoiceField(
            choices=Systems(request.COOKIES['access_token']).get_choices(),
            widget=forms.Select(
                attrs={'class': 'selectpicker', 'data-live-search': 'true', 'ng-model': 'system_id',
                       'ng-change': 'getSystemVersionById(system_id);getSystemElements(system_id); showAddComp = False;'
                                    ' removeSystemElement(-1)'}))
        self.order_fields(['system_name'])


class ComponentForm(CreationDateMixin, forms.Form):
    """
    This class is used to handle Component form
    """
    component_name = forms.CharField(max_length=255, required=True,
                                     widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    component_short_name = forms.CharField(max_length=255, required=True,
                                           widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    linked_ci_flag = forms.IntegerField(required=True,
                                     widget=forms.NumberInput(attrs={'autocomplete': 'off',
                                                                     'min': '0', 'max': '1'}))

    def __init__(self, request,*args, **kwargs):
        super(ComponentForm, self).__init__(*args, **kwargs)
        comp_type = ComponentType(request.COOKIES['access_token']).get_choices()
        self.fields['component_type_description'] = forms.ChoiceField(
            choices=comp_type,
            widget=forms.Select(
                attrs={'ng-model': 'comp_type',
                       'ng-init': 'comp_type=' + '"' +
                                  [k for k, v in dict(comp_type).items()
                                   if v == 'Application'][0] + '"'}))
        self.fields['deployment_type'] = forms.ChoiceField(
            choices=DeploymentType(request.COOKIES['access_token']).get_choices(),
            widget=forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true'}))
        self.order_fields(['component_name', 'component_short_name', 'creation_date',
                           'component_type_description', 'linked_ci_flag', 'deployment_type'])


class ComponentVersionForm(CreationDateMixin, forms.Form):
    """
    This class is used to handle Component Version form
    """
    component_version_name = forms.CharField(max_length=255, required=True,
                                             widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    #stable_flag = forms.CharField(max_length=255, required=True,
    #                              widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    artefact_store_url = forms.CharField(max_length=255, required=True,
                                         widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    source_code_repository_url = forms.CharField(max_length=255, required=True,
                                                 widget=forms.TextInput(attrs={
                                                     'autocomplete': 'off'}))
    source_tag_reference = forms.CharField(max_length=255, required=True,
                                           widget=forms.TextInput(attrs={'autocomplete': 'off'}))

    def __init__(self, request, *args, **kwargs):
        super(ComponentVersionForm, self).__init__(*args, **kwargs)
        self.fields['component_name'] = forms.ChoiceField(
            choices=Components(request.COOKIES['access_token']).get_choices(),
            widget=forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true'}))
        self.fields['artefact_store_type_desc'] = forms.ChoiceField(
            choices=ArtefactStoreType(request.COOKIES['access_token']).get_choices(),
            widget=forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true'}))
        self.order_fields(['component_name'])


class InfraTemplateForm(forms.Form):
    """
    This class is used to handle Infra Template form
    """
    infra_template_name = forms.CharField(max_length=255, required=True,
                                          widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    host_template_description = forms.CharField(max_length=255, required=True,
                                                widget=forms.TextInput(attrs={
                                                    'autocomplete': 'off'}))

    def __init__(self, request,*args, **kwargs):
        super(InfraTemplateForm, self).__init__(*args, **kwargs)
        infra_type = InfraType(request.COOKIES['access_token']).get_choices()
        default_infra_type = [k for k, v in dict(infra_type).items() if v == "Infrastructure"][0]

        self.fields['host_type_id'] = \
            forms.ChoiceField(label="Host Type", choices=HostType(request.COOKIES['access_token']).get_choices(),
                              widget=forms.Select(attrs={'class': 'selectpicker',
                                                         'data-live-search': 'true'}))
        self.fields['infrastructure_type_id'] = forms.ChoiceField(
            label="Infrastructure Type", choices=infra_type,
            widget=forms.Select(
                attrs={'ng-model': 'infrastructure_type',
                       'ng-init': 'infrastructure_type="' + str(default_infra_type) + '"'}))


class InstanceAddForm(CreationDateMixin, forms.Form):
    """
    This class is used to handle Create Instance form
    """
    INSTANCE_STATE_CHOICE = (("", "--Select--"), ("UP", "UP"), ("DOWN", "DOWN"))
    instance_name = forms.CharField(max_length=255, required=True,
                                    widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    host_instance_name = forms.CharField(max_length=255, required=True,
                                         widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    assigned_ip = forms.GenericIPAddressField(protocol='IPv4', required=True,
                                              widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    instance_state = forms.ChoiceField(required=True, choices=INSTANCE_STATE_CHOICE,
                                       widget=forms.Select(
                                           attrs={'autocomplete': 'off',
                                                  'ng-model': 'instance_state'}))
    remarks = forms.CharField(
        max_length=255, required=True, widget=forms.Textarea(attrs={
            'width': "100%", 'cols': "40", 'rows': "3", 'autocomplete': 'off'}))
    max_disks = forms.CharField(max_length=255, required=True,
                                widget=forms.TextInput(
                                    attrs={'autocomplete': 'off', 'readonly': 'readonly',
                                           'ng-model': 'infraID.max_no_disk'}))

    def __init__(self, request, *args, **kwargs):
        super(InstanceAddForm, self).__init__(*args, **kwargs)
        method_choice = MethodCreation(request.COOKIES['access_token']).get_choices()
        default_method_choice = [k for k, v in dict(method_choice).items() if v == "Manual"][0]
        self.fields['infra_template_id'] = forms.ChoiceField(
            label="Infra Template", choices=InfraTemplate(request.COOKIES['access_token']).get_choices(),
            widget=forms.Select(
                attrs={'class': 'selectpicker', 'data-live-search': 'true', 'ng-model': 'infra_id',
                       'ng-change': 'getInfraById(infra_id)'}))
        self.fields['method_creation_type_id'] = \
            forms.ChoiceField(required=False, label="Creation Method", choices=method_choice,
                              widget=forms.Select(
                                  attrs={'ng-model': 'creation_method',
                                         'ng-init': 'creation_method="' +
                                                    str(default_method_choice) + '"'}))
        self.order_fields(['instance_name', 'host_instance_name', 'assigned_ip', 'instance_state',
                           'creation_date', 'infra_template_id', 'max_disks',
                           'method_creation_type_id', 'remarks'])


class InstanceUpdateForm(forms.Form):
    """
    This class is used to handle Update Instance form
    """
    INSTANCE_STATE_CHOICE = (("", "--Select--"), ("UP", "UP"), ("DOWN", "DOWN"))
    instance_name = forms.CharField(max_length=255, required=True,
                                    widget=forms.TextInput(
                                        attrs={'autocomplete': 'off', 'readonly': 'readonly'}))
    instance_state = forms.ChoiceField(required=False, choices=INSTANCE_STATE_CHOICE,
                                       widget=forms.Select(attrs={'autocomplete': 'off'}))
    remarks = forms.CharField(
        max_length=255, required=True, widget=forms.Textarea(attrs={
            'width': "100%", 'cols': "40", 'rows': "3", 'autocomplete': 'off'}))

    def __init__(self, *args, **kwargs):
        if kwargs:
            request = kwargs.pop("request")
            cookies = request.COOKIES.get('access_token')
        else:
            cookies = args[0]["request"]
        
        super(InstanceUpdateForm, self).__init__(*args, **kwargs)
        self.fields['infra_template_id'] = \
            forms.ChoiceField(required=False, label="Infra Template",
                              choices=InfraTemplate(cookies).get_choices(),
                              widget=forms.Select(
                                  attrs={'class': 'selectpicker', 'data-live-search': 'true'}))
        self.order_fields(['instance_name', 'instance_state', 'infra_template_id'])



class NetworkSetForm(forms.Form):
    """
    This class is used to handle Network Set Form
    """
    network_set_name = forms.CharField(
        max_length=255, required=True,
        widget=forms.TextInput(
            attrs={'autocomplete': 'off', 'ng-cloak': 'True',
                   'value': '(~HostSite.host_site_name~)_(~hostSub.host_subscription_key~)'
                            '_(~EnvType.environment_type_name~)_(~SysEleType.system_element_type_name~)', 'readonly': 'readonly'}))

    subnet = forms.CharField(max_length=255, required=True,
                                    widget=forms.TextInput(
                                        attrs={'autocomplete': 'off'}))
    ip_start = forms.CharField(max_length=255, required=True,
                                    widget=forms.TextInput(
                                        attrs={'autocomplete': 'off'}))
    ip_end = forms.CharField(max_length=255, required=True,
                                    widget=forms.TextInput(
                                        attrs={'autocomplete': 'off'}))

    

class hostTypeForm(forms.Form):
    """
    This is to handle host Type Form
    """

    host_name = forms.CharField(max_length=255, required=True,
                                widget=forms.TextInput( attrs ={'autocomplete':'off'}))
    

class hostSubForm(forms.Form):
    """
    This is to handle Host Subscription Form
    """

    host_subscription_name = forms.CharField(
        max_length=255, required=True,
        widget=forms.TextInput(
            attrs={'autocomplete': 'off', 'ng-cloak': 'True',
                   'value': '(~hostRegion.host_region_name~)_(~SysNetworkSet.system_network_set_name~)'
                            '_(~EnvSub.environment_subscription_type_name~)_(~EnvType.environment_type_short_name~)', 'readonly': 'readonly'}))

    host_subscription_key = forms.CharField(max_length=255, required=True,
                              widget=forms.TextInput(attrs={'autocomplete':'off'}))


class hostRegionForm(forms.Form):
    """
    This is to handle Host Region Form
    """

    host_region_name = forms.CharField(max_length=255, required=True,
                              widget=forms.TextInput(attrs={'autocomplete':'off'}))

    host_region_description = forms.CharField(max_length=255, required=True,
                              widget=forms.TextInput(attrs={'autocomplete':'off'}))

    def __init__(self, request ,*args, **kwargs):
        super(hostRegionForm, self).__init__(*args, **kwargs)

        self.fields['host_type'] = forms.ChoiceField(
            choices=HostType(request.COOKIES['access_token']).get_choices(),
            widget=forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true'}))


class hostSiteForm(forms.Form):
    """
    This is to handle Host Site Form
    """

    host_site_name = forms.CharField(max_length=255, required=True,
                              widget=forms.TextInput(attrs={'autocomplete':'off'}))

    host_site_description = forms.CharField(max_length=255, required=True,
                              widget=forms.TextInput(attrs={'autocomplete':'off'}))

    def __init__(self, request, *args, **kwargs):
        super(hostSiteForm, self).__init__(*args, **kwargs)

        self.fields['host_region'] = forms.ChoiceField(
            choices=HostRegion(request.COOKIES['access_token']).get_choices(),
            widget=forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true'}))


