"""
Author       : Yogaraja Gopal
Creation Date: 17-01-2018
Usage        : This file is used to handle the form Model
"""
import datetime
from django import forms
from django.contrib.admin import widgets
from esmt.api.choice_list import Releases, get_release_status


class ReleaseAddForm(forms.Form):
    """
    This class defines the Release Add Form
    """
    release_name = forms.CharField(max_length=255, required=True,
                                   widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    release_owner = forms.CharField(max_length=255, required=True,
                                    widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    release_summary = forms.CharField(max_length=255, required=True,
                                      widget=forms.Textarea(
                                          attrs={'width': "100%", 'cols': "40",
                                                 'rows': "3", 'autocomplete': 'off'}))


class ReleaseVersionAddForm(forms.Form):
    """
    This class defines the Release Version Add Form
    """
    release_version_name = forms.CharField(max_length=255, required=True,
                                           widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    remarks = forms.CharField(max_length=255, required=True,
                              widget=forms.Textarea(attrs={'width': "100%", 'cols': "40",
                                                           'rows': "3", 'autocomplete': 'off'}))

    def __init__(self, rel_name,request, *args, **kwargs):
        super(ReleaseVersionAddForm, self).__init__(*args, **kwargs)
        self.rel_name = rel_name
        self.fields['release_name'] = forms.ChoiceField(
            choices=Releases(request.COOKIES['access_token']).get_choices(),
            widget=forms.Select(
                attrs={'class': 'rel-sel',
                       'ng-model': 'release_id',
                       'ng-change': 'get_release_by_id(release_id);'
                                    'showAdd = true;removeReleaseItem(-1)',
                       'ng-init': "release_id='" + str(self.rel_name) + "';showAdd = true;"}))

        self.fields['release_target_date'] = forms.DateField(
            label='Target Release Date',
            widget=widgets.AdminDateWidget())
        self.fields['release_version_status'] = forms.ChoiceField(
            choices=get_release_status(request),
            widget=forms.Select(attrs={'class': 'rel-sel',
                                       'ng-model': 'release_version_status',
                                       'ng-init': 'release_version_status="7"'}))
        self.order_fields(['release_name'])

    def clean_release_target_date(self):
        """
        This function is used to clean the release date to specific format
        """
        data = self.cleaned_data['release_target_date']
        data = datetime.datetime.strftime(data, '%d/%m/%y')
        return data


class CreateReleaseForm(forms.Form):
    """
    This class defines the Create Release Form
    """
    release_name = forms.CharField(max_length=255, required=True,
                                   widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    release_owner = forms.CharField(max_length=255, required=True,
                                    widget=forms.TextInput(attrs={'autocomplete': 'off'}))

    def __init__(self, *args, **kwargs):
        super(CreateReleaseForm, self).__init__(*args, **kwargs)
        self.fields['release_date'] = forms.SplitDateTimeField(widget=widgets.AdminSplitDateTime())

    def clean_release_date(self):
        """
        This function is used to clean the release date to specific format
        """
        data = self.cleaned_data['release_date']
        data = datetime.datetime.strftime(data, '%d/%m/%y %H:%M:%S')
        return data


class CreateDeploymentForm(forms.Form):
    """
    This class defines the Create Deployment Form
    """
    deployment_name = forms.CharField(label="Deployment Description", max_length=255, required=True,
                                      widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    user_name = forms.CharField(label="Deployer Name", max_length=255, required=True,
                                widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    remarks = forms.CharField(max_length=255, required=True,
                              widget=forms.Textarea(attrs={'rows': 3, 'autocomplete': 'off',
                                                           'ng-model':
                                                               'deploy_audit.deployment_remarks'}))
    status = forms.ChoiceField(choices=[('-1', '--Select--'), ('1', 'Awaiting Approval'),
                                        ('2', 'Approved'), ('3', 'In Progress')],
                               widget=forms.Select(
                                   attrs={'ng-model': 'deploy_audit.deployment_status.status_id'}),
                               required=True)

    def __init__(self, *args, **kwargs):
        super(CreateDeploymentForm, self).__init__(*args, **kwargs)
        self.fields['planned_deployment_date'] = forms.SplitDateTimeField(
            widget=widgets.AdminSplitDateTime())
        self.fields['requested_date'] = forms.SplitDateTimeField(
            widget=widgets.AdminSplitDateTime())

    def clean_planned_deployment_date(self):
        """
        This function is used to clean the planned deployment date to specific format
        """
        data = self.cleaned_data['planned_deployment_date']
        data = datetime.datetime.strftime(data, '%d/%m/%y %H:%M:%S')
        return data

    def clean_requested_date(self):
        """
        This function is used to clean the requested date to specific format
        """
        data = self.cleaned_data['requested_date']
        data = datetime.datetime.strftime(data, '%d/%m/%y %H:%M:%S')
        return data



class routeToLiveForm(forms.Form):

    def __init__(self,request , *args, **kwargs):
        super(routeToLiveForm, self).__init__(*args, **kwargs)
        self.fields['release'] = forms.ChoiceField(
            choices=sorted(Releases(request.COOKIES['access_token']).get_choices(), key=lambda x: x[1]),
            widget=forms.Select(attrs={'class': 'rel-sel', 'ng-model': 'release_data'}))

