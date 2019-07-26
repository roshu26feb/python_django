"""
Author: Yogaraja Gopal
Comment: This module is used to handle Views for env_set app
"""
import json
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView
from django.http import JsonResponse
from rest_framework import status
from esmt.api.mixins import AjaxFormMixin
from esmt.api.abstract import post_request, post_request_secure
from .conf.properties import ENV, ENV_SERVICE_LIST, ENV_DESCRIPTION
from .forms import EnvironmentSetForm


def all_env_set(request):
    """
    This function is used to render all env set view
    """
    return render(request, 'env_set/all.html', {})


class EnvironmentSetAddView(AjaxFormMixin, FormView):
    """
    This function is used to handle Environment Set Add View
    """
    form_class = EnvironmentSetForm
    template_name = 'env_set/env_set_add.html'
    success_url = reverse_lazy('env_set:all')

    def form_valid(self, form):
        response = super(EnvironmentSetAddView, self).form_valid(form)
        if self.request.is_ajax():
            post_data = dict(self.request.POST.items())
            environment_set_name = post_data['environment_set_name']
            data = {
                "environment_set_name": environment_set_name,
            }
            env_ids = []  
            for field, value in post_data.items():
                env_id = dict()
                if field.split("-")[0] == "environment_id":
                    env_id["environment_id"] = value
                    env_ids.append(env_id)
            data["environment_ids"] = env_ids

            print(data)
                
            resp = post_request_secure("/api/v1/environment_set", data, self.request.COOKIES.get('access_token'))
            if resp.status_code == status.HTTP_200_OK:
                resp_data = json.loads(resp.text)
                resp_data["url"] = reverse_lazy('env_set:all')
                return JsonResponse(resp_data, status=resp.status_code, safe=False)
            return JsonResponse(resp.text, status=resp.status_code, safe=False)
        return response


def sit(request):
    """ This function is used to present the Main ECT Page """
    store_list = {}
    for region, env in ENV.items():
        env_list = []
        for key in env.keys():
            env_list.append(key)
        store_list[region] = env_list
    env_region = ENV
    services = ENV_SERVICE_LIST
    env_description = ENV_DESCRIPTION
    context_data = {'store_list': store_list, 'env': env_region, 'services': services,
                    'env_desc': env_description}
    return render(request, 'env_set/sit.html', context=context_data)


def two(request):
    """ This function is used to render sit two page """
    return render(request, 'env_set/sittwo.html', {})


def uat(request):
    """ This function is used to render UAT page"""
    return render(request, 'env_set/uat.html', {})


def pre_prod(request):
    """ This function is used to render pre-prod page """
    return render(request, 'env_set/pre_prod.html', {})
