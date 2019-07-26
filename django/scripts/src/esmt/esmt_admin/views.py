"""
Author: Yogaraja Gopal
Date : 12-04-2018
This module contains the Views used for Esmt Admin
"""
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView
from rest_framework import status
from esmt.api.mixins import AjaxFormMixin
from esmt.api.abstract import post_request, put_request, get_request ,get_request_secure,post_request_secure,put_request_secure
from esmt.api.choice_list import get_parameter_type_name
from .forms import ParameterForm, ReferenceDataForm, AddUserForm, UserRoleForm


def user_roles(request):
    """
    This function is used to handle the list of Users View
    """
    role_resp = get_request_secure("/api/v1/role" ,  request.COOKIES.get('access_token'))
    user_resp = get_request_secure("/api/v1/user" ,  request.COOKIES.get('access_token'))
    try:
        role_list = []
        users = []
        err_msg = ""
        if role_resp.status_code == status.HTTP_200_OK and \
                user_resp.status_code == status.HTTP_200_OK:
            role_data = json.loads(role_resp.text)
            user_data = json.loads(user_resp.text)
            users = user_data["users"]
            for role in role_data["roles"]:
                role_list.append(role["role_name"])
        else:
            err_msg = 'Unable to get User/Role Details'
    except:
        role_list = []
        users = []
        err_msg = 'Unable to connect to Delivery DB'
    context_data = {'roles': role_list, 'users': users, 'error': err_msg}

    return render(request, 'esmt_admin/user_roles.html', context=context_data)


def ref_data_manager(request):
    """
    This function is used to render reference data manager screen
    """
    return render(request, 'esmt_admin/ref_data_manager.html', {})


def deploy_parameter(request):
    """
    This function is used to render Deployment Parameter screen
    """
    return render(request, 'esmt_admin/deploy_parameter.html', {})


def view_user(request):
    """
    This function is used to render List of Users screen
    """
    return render(request, 'esmt_admin/view_user.html', {})


class AddUserView(AjaxFormMixin, FormView):
    """
    This function is used to handle User Add View
    """
    form_class = AddUserForm
    template_name = 'esmt_admin/add_user.html'
    success_url = reverse_lazy('esmt_admin:user_role_add')

    def form_valid(self, form):
        response = super(AddUserView, self).form_valid(form)
        if self.request.is_ajax():
            display_name = form.cleaned_data["display_name"]
            user_name = form.cleaned_data["user_name"]
            email_address = form.cleaned_data["email_address"]

            print(form.cleaned_data)
            data = {
                "user_display_name": display_name,
                "user_name": user_name,
                "email_address": email_address,
                "user_roles": ['1']
            }

            resp = post_request("/api/v1/user", data)
            if resp.status_code == status.HTTP_200_OK:
                resp_data = json.loads(resp.text)
                self.request.session["user_id"] = resp_data["user_id"]
                resp_data["url"] = reverse_lazy('esmt_admin:user_role_add')
                return JsonResponse(resp_data, status=resp.status_code, safe=False)
            return JsonResponse(resp.text, status=resp.status_code, safe=False)
        return response


class UserRoleAddView(AjaxFormMixin, FormView):
    """
    This function is used to handle Infrastructure Add View
    """
    form_class = UserRoleForm
    template_name = 'esmt_admin/user_role_add.html'
    success_url = reverse_lazy('esmt_admin:user_roles')

    def get_form_kwargs(self):
        kwargs = super(UserRoleAddView, self).get_form_kwargs()
        kwargs['user_id'] = self.request.session.pop('user_id', '')
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        response = super(UserRoleAddView, self).form_valid(form)
        if self.request.is_ajax():
            user_role_list = self.request.POST.getlist('user_roles')
            user_id = form.cleaned_data["user"]

            data = {
                "user_id": user_id,
                "user_roles": user_role_list
            }
            resp = put_request("/api/v1/user", data)
            if resp.status_code == status.HTTP_200_OK:
                resp_data = json.loads(resp.text)
                resp_data["url"] = reverse_lazy('esmt_admin:user_roles')
                return JsonResponse(resp_data, status=resp.status_code, safe=False)
            return JsonResponse(resp.text, status=resp.status_code, safe=False)
        return response


class ReferenceDataView(FormView):
    """
    This class is used to render Reference data View
    """
    form_class = ReferenceDataForm
    template_name = 'esmt_admin/reference_data.html'
    success_url = reverse_lazy('esmt_admin:reference_data')
  


def parameter_add_update(request, parameter_id=''):
    """
    This function is used to render Instance update view and handle instance update form submission
    """
    if request.method == 'POST':
        request.POST = request.POST.copy()
        request.POST['request'] = request
        form = ParameterForm(request.POST)
        if form.is_valid():
            if request.is_ajax():
                post_data = dict(request.POST.items())
                parameter_name = form.cleaned_data["parameter_name"]
                parameter_internal_name = form.cleaned_data["parameter_internal_name"]
                mandatory = form.cleaned_data["mandatory"]
                active = form.cleaned_data["active"]
                parameter_type = form.cleaned_data["parameter_type"]
                parameter_type_name = get_parameter_type_name(parameter_type , request)

                if mandatory == 'false':
                    mandatory = ""
                if active == 'false':
                    active = ""
                data = {
                    "parameter_type_id": parameter_type,
                    "mandatory": bool(mandatory),
                    "active": bool(active),
                    "component_type_id": post_data["component_type_id"],
                    "component_id": post_data["component_id"]
                }
                param_values = []
                if parameter_type_name.upper() == 'NUMBER':
                    param_values.append(
                        "DECIMAL(" + post_data["value-0"] + "," + post_data["value-1"] + ")")
                elif parameter_type_name.upper() == 'FREE TEXT':
                    param_values.append("VARCHAR(" + post_data["value-0"] + ")")
                elif parameter_type_name.upper() == 'BOOLEAN':
                    param_values.append("True")
                    param_values.append("False")
                else:
                    for key, value in post_data.items():
                        if key.split('-')[0] == 'value':
                            param_values.append(value)
                #if param_values:
                data["parameter_values"] = param_values

                if parameter_id:
                    data["parameter_name"] = parameter_name
                    data["parameter_internal_name"] = parameter_internal_name
                    data["parameter_id"] = parameter_id
                    resp = put_request_secure("/api/v1/parameter", data ,  request.COOKIES.get('access_token'))
                else:
                    data["parameter_name"] = parameter_name
                    data["parameter_internal_name"] = parameter_internal_name
                    resp = post_request_secure("/api/v1/parameter", data ,  request.COOKIES.get('access_token'))

                if resp.status_code == status.HTTP_200_OK:
                    resp_data = json.loads(resp.text)
                    resp_data["url"] = reverse_lazy('esmt_admin:deploy_parameter')
                    return JsonResponse(resp_data, status=resp.status_code, safe=False)
                return JsonResponse(resp.text, status=resp.status_code, safe=False)
    else:
        form = ParameterForm(request=request)
    return render(request, 'esmt_admin/parameter_add_edit.html', {'form': form,
                                                                  'parameter_id': parameter_id})
