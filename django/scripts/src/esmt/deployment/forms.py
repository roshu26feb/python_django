"""
Author       : Yogaraja Gopal
Creation Date: 17-01-2018
Usage        : This file is used to handle the form Model
"""
from datetime import datetime
from datetime import timedelta
from django import forms
from datetimewidget.widgets import DateTimeWidget, DateWidget
from esmt.api.choice_list import get_environment_by_system_id, get_parameters, InfraTemplate, \
    HostType, application_components


class RequestDeploymentForm(forms.Form):
    """
    This Class is used to model the Deployment request form
    """
    system = forms.CharField(max_length=255, required=True,
                             widget=forms.TextInput(
                                 attrs={'autocomplete': 'off', 'readonly': 'readonly',
                                        'class': 'form-control'}))
    system.group = 1
    system_id = forms.CharField(max_length=255, required=True, widget=forms.HiddenInput(attrs={'ng-model': 'sys_id'}))
    system_version_id = forms.CharField(max_length=255, required=True, widget=forms.HiddenInput(attrs={'ng-model': 'sys_version_id','data-internal-name':'system_version_id'}))
    system_element_id2 = forms.CharField(max_length=255, required=True, widget=forms.HiddenInput(attrs={'ng-model': 'sys_elem_id','data-internal-name':'sys_elem_id'}))
    system_version = forms.CharField(max_length=255, required=True,
                                     widget=forms.TextInput(
                                         attrs={'autocomplete': 'off', 'readonly': 'readonly',
                                                'class': 'form-control'}))
    system_version.group = 1
    system_element_id = forms.CharField(max_length=255, required=True, label='System Element',
                                        widget=forms.TextInput(
                                            attrs={'autocomplete': 'off', 'readonly': 'readonly',
                                                   'class': 'form-control'}))
    system_element_id.group = 1

    deployment_name = forms.CharField(max_length=255, required=True, label='Deployment Title',
                                      widget=forms.TextInput(
                                          attrs={'autocomplete': 'off', 'class': 'form-control','labelerror':'Deployment Title is required.'}))
    deployment_name.group = 2
    user_name = forms.CharField(max_length=255, required=True, label="Requestor",
                                widget=forms.TextInput(
                                    attrs={'autocomplete': 'off', 'class': 'form-control','labelerror':'Requestor is required.'}))
    user_name.group = 2

    infra_code_flag = forms.BooleanField(label='Infrastructure', required=False,
                                         widget=forms.CheckboxInput(
                                             attrs={'ng-model': 'infra', 'ng-init': 'infra=false',
                                                    'ng-change': 'clearInfraComp();','ng-required':'(!(infraConf || infra || app))' ,'labelerror':'Infrastructure ,Infrastructure Config or Application is required.'}))
    infra_code_flag.group = 5
    infra_config_flag = forms.BooleanField(label='Infrastructure Config', required=False,
                                           widget=forms.CheckboxInput(
                                               attrs={'ng-model': 'infraConf',
                                                      'ng-init': 'infraConf=false','ng-click': 'clearInfraConfigComp()' ,'ng-required':'(!(infraConf || infra || app))' ,'labelerror':''}))

    infra_config_flag.group = 5
    app_flag = forms.BooleanField(label='Application', required=False, initial=True,
                                  widget=forms.CheckboxInput(
                                      attrs={'ng-model': 'app', 'ng-init': 'app=false',
                                             'ng-click': 'clearAppComp()','ng-required':'(!(infraConf || infra || app))' ,'labelerror':''}))
    app_flag.group = 5
    deployment_remarks = forms.CharField(
        max_length=255, required=True, label='Comments',
        widget=forms.Textarea(attrs={'rows': 3, 'autocomplete': 'off', 'class': 'form-control'}))
    deployment_remarks.group = 6

    def __init__(self, *args, **kwargs):
        if kwargs:
            system_id = kwargs.pop("system_id")
            component_ids = kwargs.pop("component_ids")
            component_type_ids = kwargs.pop("component_type_ids")
            app_comp_map = kwargs.pop("app_comp_map")
            app_comp = kwargs.pop("app_components")
            infra_conf_comp = kwargs.pop("infra_conf_components")
            infra_components = kwargs.pop("infra_components")
            system_element_short_name = kwargs.pop("sys_element_short_name") 
            component_info = kwargs.pop("component_info")
            request = kwargs.pop("request") 
        else:
            system_id = args[0]["system_id"]
            system_element_short_name = ""
            request = args[0]["request"]
        super(RequestDeploymentForm, self).__init__(*args, **kwargs)

        if kwargs:
            #app_comp = application_components(component_ids)
            if len(app_comp) >= 1:
                self.fields['available_application'] = forms.MultipleChoiceField(
                    required=True, choices=app_comp,
                    widget=forms.CheckboxSelectMultiple(attrs={'ng-comp-name':'comp', 'ng-required':'check_list_app.length == 0 && app==true' , 'ng-click': 'compVal($event)','class': 'input_component_checkbox' , 'labelerror':'Application deployment component type is selected for deployment, please select an available application.'}))
                self.fields['available_application'].group = 3
            if len(infra_conf_comp) >= 1:
                self.fields['available_infra_config'] = forms.MultipleChoiceField(
                    required=True, choices=infra_conf_comp,
                    widget=forms.CheckboxSelectMultiple(attrs={'ng-comp-name':'infra_config',  'ng-required':'check_list_infraconfig.length == 0 && infraConf==true' , 'ng-click': 'compVal($event)','class': 'input_component_checkbox', 'labelerror':'Infrastructure Configuration deployment component type is selected for deployment, please select an available infrastructure configuration.'}))
                self.fields['available_infra_config'].group = 9
            parameter_fields = get_parameters("component_type", component_type_ids , request.COOKIES['access_token'])
            for parameter_field in get_parameters("component", component_ids , request.COOKIES['access_token']):
                parameter_fields.append(parameter_field)
                

            for param_field in parameter_fields:
                if(param_field.get("comp_id", "true") == "true" and param_field.get("infraConf_comp_id", "true") == "true" and param_field.get("infra_comp_id", "true") == "true"):
                    comp_type = param_field.get("comp_type", "true")
                    comp_id = 0 
                else:
                    if('comp_id' in param_field):
                        comp_type = 'app'
                        comp_id = str(app_comp_map[param_field["comp_id"]])
                    elif('infraConf_comp_id' in param_field):
                        comp_type = 'infraConf'
                        comp_id = str(app_comp_map[param_field["infraConf_comp_id"]])
                    elif('infra_comp_id' in param_field):
                        comp_type = 'infra'
                        comp_id = param_field.get("infra_comp_id", "true")


                if param_field["type"].upper() == 'LIST SINGLE' or \
                   param_field["type"].upper() == 'BOOLEAN':
                    self.fields[param_field["name"]] = \
                        forms.ChoiceField(
                            label=param_field["label"], choices=param_field["choices"],
                            required=param_field["mandatory"],
                            widget=forms.Select(
                                attrs={
                                    'class': 'form-control',
                                    'data-internal-name': param_field["parameter_internal_name"],
                                    'data-comp-type':comp_type,
                                    'data-comp-id':comp_id,
                                    'ngIf': param_field.get("comp_type", "true") 
                                    if param_field.get("comp_id", "true") == "true" and param_field.get("infraConf_comp_id", "true") == "true" and param_field.get("infra_comp_id", "true") == "true"
                                    else "comp"+ str(app_comp_map[param_field["comp_id"]]) + "==true && app==true" if param_field.get("infraConf_comp_id", "true") == "true" and param_field.get("infra_comp_id", "true") == "true" else "infra_config"+ str(app_comp_map[param_field["infraConf_comp_id"]]) +"==true && infraConf==true" if param_field.get("infra_comp_id", "true") == "true" else "infra==true" ,'labelerror':param_field["label"]+' is required. '}))

                    self.fields[param_field["name"]].group = 7

                    if(param_field.get("comp_id", "true") == "true" and param_field.get("infraConf_comp_id", "true") == "true" and param_field.get("infra_comp_id", "true") == "true"):
                        self.fields[param_field["name"]].elem_comp_type = param_field.get("comp_type", "true")
                    else:
                         if('comp_id' in param_field):
                             self.fields[param_field["name"]].elem_comp_app = True
                         elif('infraConf_comp_id' in param_field):
                             self.fields[param_field["name"]].elem_comp_infraConf = True
                         elif('infra_comp_id' in param_field):
                             self.fields[param_field["name"]].elem_comp_infra = True


                elif param_field["type"].upper() == 'LIST MULTI':
                    self.fields[param_field["name"]] = \
                        forms.MultipleChoiceField(
                            label=param_field["label"], choices=param_field["choices"],
                            required=param_field["mandatory"],
                            widget=forms.SelectMultiple(
                                attrs={'class': 'form-control list-multiple',
                                'data-internal-name': param_field["parameter_internal_name"],
                                'data-comp-type':comp_type,
                                'data-comp-id':comp_id,
                                       'ngIf': param_field.get("comp_type", "true")
                                       if param_field.get("comp_id", "true") == "true" and param_field.get("infraConf_comp_id", "true") == "true" and param_field.get("infra_comp_id", "true") == "true"      
                                       else "comp"+ str(app_comp_map[param_field["comp_id"]]) + "==true && app==true" if param_field.get("infraConf_comp_id", "true") == "true" and param_field.get("infra_comp_id", "true") == "true" else "infra_config"+ str(app_comp_map[param_field["infraConf_comp_id"]]) +"==true && infraConf==true" if param_field.get("infra_comp_id", "true") == "true" else "infra==true" ,'labelerror':param_field["label"]+' is required.'}))
                    self.fields[param_field["name"]].group = 7

                    if(param_field.get("comp_id", "true") == "true" and param_field.get("infraConf_comp_id", "true") == "true" and param_field.get("infra_comp_id", "true") == "true"):
                        self.fields[param_field["name"]].elem_comp_type = param_field.get("comp_type", "true")
                    else:
                         if('comp_id' in param_field):
                             self.fields[param_field["name"]].elem_comp_app = True
                         elif('infraConf_comp_id' in param_field):
                             self.fields[param_field["name"]].elem_comp_infraConf = True
                         elif('infra_comp_id' in param_field):
                             self.fields[param_field["name"]].elem_comp_infra = True

                elif param_field["type"].upper() == 'NUMBER':
                    self.fields[param_field["name"]] = \
                        forms.CharField(
                            label=param_field["label"], required=param_field["mandatory"],
                            widget=forms.NumberInput(
                                attrs={
                                    'autocomplete': 'off', 'min': param_field["min"],
                                    'data-internal-name': param_field["parameter_internal_name"],
                                    'onkeydown':'javascript: return event.keyCode == 69 ? false : true',
                                    'max': param_field["max"],
                                    'data-comp-type':comp_type,
                                    'data-comp-id':comp_id,
                                    'ngIf': param_field.get("comp_type", "true") if param_field.get("comp_id", "true") == "true" and param_field.get("infraConf_comp_id", "true") == "true" and param_field.get("infra_comp_id", "true") == "true"
                                    else "comp"+ str(app_comp_map[param_field["comp_id"]]) + "==true && app==true" if param_field.get("infraConf_comp_id", "true") == "true" and param_field.get("infra_comp_id", "true") == "true" else "infra_config"+ str(app_comp_map[param_field["infraConf_comp_id"]]) +"==true && infraConf==true" if param_field.get("infra_comp_id", "true") == "true" else "infra==true" ,'labelerror':param_field["label"]+'  should be in the range of '+param_field["min"]+' - '+param_field["max"]}))
                    self.fields[param_field["name"]].group = 7

                    if(param_field.get("comp_id", "true") == "true" and param_field.get("infraConf_comp_id", "true") == "true" and param_field.get("infra_comp_id", "true") == "true"):
                        self.fields[param_field["name"]].elem_comp_type = param_field.get("comp_type", "true")
                    else:
                         if('comp_id' in param_field):
                             self.fields[param_field["name"]].elem_comp_app = True
                         elif('infraConf_comp_id' in param_field):
                             self.fields[param_field["name"]].elem_comp_infraConf = True
                         elif('infra_comp_id' in param_field):
                             self.fields[param_field["name"]].elem_comp_infra = True

                elif param_field["type"].upper() == 'FREETEXT':
                    self.fields[param_field["name"]] = \
                        forms.CharField(
                            max_length=param_field["size"], required=param_field["mandatory"],
                            label=param_field["label"],
                            widget=forms.TextInput(
                                attrs={
                                    'autocomplete': 'off', 'class': 'form-control',
                                    'data-internal-name': param_field["parameter_internal_name"],
                                    'data-comp-type':comp_type,
                                    'data-comp-id':comp_id,
                                    #'data-comp-id': param_field.get("comp_id", "true"),
                                    'ngIf': param_field.get("comp_type", "true") if param_field.get("comp_id", "true") == "true" and param_field.get("infraConf_comp_id", "true") == "true" and param_field.get("infra_comp_id", "true") == "true"
                                    else "comp"+ str(app_comp_map[param_field["comp_id"]]) + "==true && app==true" if param_field.get("infraConf_comp_id", "true") == "true" and param_field.get("infra_comp_id", "true") == "true" else "infra_config"+ str(app_comp_map[param_field["infraConf_comp_id"]]) +"==true && infraConf==true" if param_field.get("infra_comp_id", "true") == "true" else "infra==true",
                                      'value': '(~ calc_instance_name ~)' if param_field["label"].lower().replace("_", " ") == "host name" else '' ,'labelerror':param_field["label"]+' is required.'}))
                    if param_field["label"].lower().replace("_", " ") == "host name":
                        self.fields[param_field["name"]].widget.attrs['readonly'] = True
                    
                    self.fields[param_field["name"]].group = 7

                    if(param_field.get("comp_id", "true") == "true" and param_field.get("infraConf_comp_id", "true") == "true" and param_field.get("infra_comp_id", "true") == "true"):
                        self.fields[param_field["name"]].elem_comp_type = param_field.get("comp_type", "true")
                    else:
                         if('comp_id' in param_field):
                             self.fields[param_field["name"]].elem_comp_app = True
                         elif('infraConf_comp_id' in param_field):
                             self.fields[param_field["name"]].elem_comp_infraConf = True
                         elif('infra_comp_id' in param_field):
                             self.fields[param_field["name"]].elem_comp_infra = True

                    
                elif param_field["type"].upper() == 'DATE TIME':
                    self.fields[param_field["name"]] = \
                        forms.DateTimeField(
                            label=param_field["label"],required=param_field["mandatory"],
                            widget=DateTimeWidget(
                                attrs={'class': 'form-control',
                                'data-internal-name': param_field["parameter_internal_name"],
                                'data-comp-type':comp_type,
                                'data-comp-id':comp_id,
                                       'ngIf': param_field.get("comp_type", "true")
                                       if param_field.get("comp_id", "true") == "true" and param_field.get("infraConf_comp_id", "true") == "true" and param_field.get("infra_comp_id", "true") == "true"
                                       else "comp"+ str(app_comp_map[param_field["comp_id"]]) + "==true && app==true" if param_field.get("infraConf_comp_id", "true") == "true" and param_field.get("infra_comp_id", "true") == "true" else "infra_config"+ str(app_comp_map[param_field["infraConf_comp_id"]]) +"==true && infraConf==true" if param_field.get("infra_comp_id", "true") == "true" else "infra==true" ,'labelerror':param_field["label"]+' is required.'}, usel10n=True,
                                bootstrap_version=3))
                    self.fields[param_field["name"]].group = 7
                    
                    if(param_field.get("comp_id", "true") == "true" and param_field.get("infraConf_comp_id", "true") == "true" and param_field.get("infra_comp_id", "true") == "true"):
                        self.fields[param_field["name"]].elem_comp_type = param_field.get("comp_type", "true")
                    else:
                         if('comp_id' in param_field):
                             self.fields[param_field["name"]].elem_comp_app = True
                         elif('infraConf_comp_id' in param_field):
                             self.fields[param_field["name"]].elem_comp_infraConf = True
                         elif('infra_comp_id' in param_field):
                             self.fields[param_field["name"]].elem_comp_infra = True

                elif param_field["type"].upper() == 'DATE':
                    self.fields[param_field["name"]] = \
                        forms.DateTimeField(
                            label=param_field["label"],required=param_field["mandatory"],
                            widget=DateWidget(
                                attrs={
                                    'class': 'form-control',
                                    'data-internal-name': param_field["parameter_internal_name"],
                                    'data-comp-type':comp_type,
                                    'data-comp-id':comp_id,
                                    'ngIf': param_field.get("comp_type", "true")  if param_field.get("comp_id", "true") == "true" and param_field.get("infraConf_comp_id", "true") == "true" and param_field.get("infra_comp_id", "true") == "true"
                                    else "comp"+ str(app_comp_map[param_field["comp_id"]]) + "==true && app==true" if param_field.get("infraConf_comp_id", "true") == "true" and param_field.get("infra_comp_id", "true") == "true" else "infra_config"+ str(app_comp_map[param_field["infraConf_comp_id"]]) +"==true && infraConf==true" if param_field.get("infra_comp_id", "true") == "true" else "infra==true" ,'labelerror':param_field["label"]+' is required.'}, usel10n=True,
                                bootstrap_version=3))
                    self.fields[param_field["name"]].group = 7
                    
                    if(param_field.get("comp_id", "true") == "true" and param_field.get("infraConf_comp_id", "true") == "true" and param_field.get("infra_comp_id", "true") == "true"):
                        self.fields[param_field["name"]].elem_comp_type = param_field.get("comp_type", "true")
                    else:
                         if('comp_id' in param_field):
                             self.fields[param_field["name"]].elem_comp_app = True
                         elif('infraConf_comp_id' in param_field):
                             self.fields[param_field["name"]].elem_comp_infraConf = True
                         elif('infra_comp_id' in param_field):
                             self.fields[param_field["name"]].elem_comp_infra = True

        self.fields['environment_id'] = \
            forms.ChoiceField(label="Environment to Deploy To",
                              choices=get_environment_by_system_id(system_id , request.COOKIES['access_token']),
                              widget=forms.Select(
                                  attrs={'class': 'selectpicker form-control',
                                         'data-live-search': 'true', 'ng-model': 'env', 'ng-init':'env;sys_id;sys_version_id;sys_elem_id',
                                         'ng-change': 'getInstanceFromEnv(env);getNetworkSetName(env);getInstanceAllocation(env)' ,'labelerror':'Environment to Deploy To is required.', 'data-internal-name': 'environment_id',
                                 }))


        self.fields['environment_id'].group = 3
        host_choice = HostType(request.COOKIES['access_token']).get_choices()
        self.fields['host'] = \
            forms.ChoiceField(label="Host", initial="6", choices=host_choice,
                              widget=forms.Select(
                                  attrs={'class': 'form-control', 'ng-model': 'host',
                                         'ng-init': 'host="' +
                                                    str([k for k, v in dict(host_choice).items()
                                                         if v == 'Azure - EU']) + '"',
                                         'ng-readonly': '!infra', 'ng-init': 'getHostSite(host)',
                                         'ng-change':'getHostSite(host);checkAzure();'}))
        self.fields['host'].group = 3
        self.fields['infra_template_id'] = \
            forms.ChoiceField(label="Infra Template", required=False, choices=InfraTemplate(request.COOKIES['access_token']).get_choices(),
                              widget=forms.Select(
                                  attrs={'class': 'selectpicker form-control',
                                         'ng-model': 'infraID', 'data-live-search': 'true',
                                         'ng-readonly': '!infra','ng-change': 'getSysEle(system_id)','labelerror':'Infra Template is required.'}))
        self.fields['infra_template_id'].group = 3
        
        self.fields['instance_name'] = forms.CharField(
            label='Instance Name', required=False, widget=forms.TextInput(
                attrs={'autocomplete': 'off', 'ng-cloak': 'True', 'class': 'form-control',
                        'value': '(~ calc_instance_name ~)', 'readonly': 'readonly',
                        'ng-init': 'setShortName("' + system_element_short_name.lower() + '")'}))
        self.fields['instance_name'].group = 8 

        self.fields['planned_deployment_date'] = forms.DateTimeField(
            label='Target Deployment Date', initial=datetime.today() + timedelta(days=1),
            widget=DateTimeWidget(attrs={'id': 'id_planned_date', 'class': 'form-control'},
                                  usel10n=True, bootstrap_version=3))
        self.fields['planned_deployment_date'].group = 4
        self.order_fields(['system', 'system_version', 'system_element_id', 'deployment_name',
                           'user_name', 'environment_id', 'planned_deployment_date', 'host',
                           'infra_template_id', 'infra_code_flag', 'infra_config_flag',
                           'app_flag', 'deployment_remarks'])

    def clean_planned_deployment_date(self):
        """
        This function is used to clean the planned deployment date to specific format
        """
        data = self.cleaned_data['planned_deployment_date']
        data = datetime.strftime(data, '%d/%m/%y %H:%M:%S')
        return data
        
     
  
    def group1(self):
        """
        This function is used to group, group 1 fields
        """
        return filter(lambda x: x.group == 1, self.fields.values())

    def group2(self):
        """
        This function is used to group, group 2 fields
        """
        return filter(lambda x: x.group == 2, self.fields.values())

    def group3(self):
        """
        This function is used to group, group 3 fields
        """
        return filter(lambda x: x.group == 3, self.fields.values())

    def group4(self):
        """
        This function is used to group, group 4 fields
        """
        return filter(lambda x: x.group == 4, self.fields.values())

    def group5(self):
        """
        This function is used to group, group 5 fields
        """
        return filter(lambda x: x.group == 5, self.fields.values())

    def group6(self):
        """
        This function is used to group, group 6 fields
        """
        return filter(lambda x: x.group == 6, self.fields.values())

    def group7(self):
        """
        This function is used to group, group 7 fields
        """
        return filter(lambda x: x.group == 7, self.fields.values())

    def group8(self):
        """
        This function is used to group, group 8 fields
        """
        return filter(lambda x: x.group == 8, self.fields.values())