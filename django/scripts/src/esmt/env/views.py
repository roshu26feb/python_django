"""
Author: Yogaraja Gopal
This module is used to handle view for env app
"""
import json
import time
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import FormView
from rest_framework import status
from esmt.api.abstract import post_request
from esmt.api.mixins import AjaxFormMixin
from .conf import properties as env_prop
from .conf import properties_r2 as r2_env_prop
from .conf.solar7_properties import SOLAR7_ENV
from .conf.plato_properties import PLATO_ENV
from .common.process_command import get_data_from_file
from .models import Server, ServiceGroup
from .forms import EnvironmentForm
from esmt.api.abstract import post_request, get_request, post_request_secure,get_request_secure

def all_env(request):
    """
    This function is used to render all env view
    """
    return render(request, 'env/all.html', {})


def r3_env(request):
    """
    This function is used to render r3 environment view
    """
    now = time.strftime("%c")
    stores = sorted(env_prop.SOC_STORES.keys(), key=lambda item: int(item.split('.')[2]))
    client_details = env_prop.SOC_STORES
    services = env_prop.SERVICES
    mount = get_data_from_file('mount')
    facts = get_data_from_file('facts')
    repl = get_data_from_file('replication')

    context_data = {'stores': stores, 'env': client_details, 'services': services,
                    'mount': mount, 'facts': facts, 'replication_status': repl, 'showtime': now}
    return render(request, 'env/r3.html', context=context_data)


def r3_tab(request):
    """
    This function is used to render r3 Tab environment view
    """
    stores = Server.objects.prefetch_related('mounttimestamp_set').all()
    mount = Server.objects.prefetch_related('mounttimestamp_set').all()
    context_data = {'stores': stores, 'mount': mount}
    return render(request, 'env/r3_tab.html', context=context_data)


def r3_mod(request):
    """
    This function is used to render r3_mod environment view
    """
    stores = Server.objects.filter(env_type="socrates", app="env", sub_app="r3",
                                   store_server__server_ip=None)
    service_group = Server.objects.filter(env_type="socrates", app="env",
                                          sub_app="r3").prefetch_related("service_group")
    services = ServiceGroup.objects.prefetch_related("services_set").all()
    service_instance = Server.objects.filter(env_type="socrates", app="env",
                                             sub_app="r3").prefetch_related("serviceinstance_set")
    context_data = {'stores': stores, 'service_group': service_group, 'services': services,
                    'service_instance': service_instance}
    return render(request, 'env/r3_tab.html', context=context_data)


def r2_env(request):
    """
    This function is used to render r2 environment view
    """
    now = time.strftime("%c")
    stores = sorted(r2_env_prop.SOC_STORES.keys(), key=lambda item: int(item.split('.')[2]))
    client_details = r2_env_prop.SOC_STORES
    services = r2_env_prop.SERVICES
    mount = get_data_from_file('mount_r2')
    facts = get_data_from_file('facts_r2')
    repl = get_data_from_file('replication_r2')

    context_data = {'stores': stores, 'env': client_details, 'services': services,
                    'mount': mount, 'facts': facts, 'replication_status': repl, 'showtime': now}
    return render(request, 'env/r2.html', context=context_data)


def plato(request):
    """
    This function is used to render plato environment view
    """
    plato_env = sorted(PLATO_ENV.keys(), key=lambda item: int(item.split('.')[2]))
    plato_env_details = PLATO_ENV
    mount = get_data_from_file('plato_mount')
    context_data = {'plato_env': plato_env, 'plato_env_details': plato_env_details, 'mount': mount}
    return render(request, 'env/plato.html', context=context_data)


def soc_aus(request):
    """
    This function is used to render socrates AU view
    """
    context_data = {'nav': 'socAU'}
    return render(request, 'env/socAU.html', context=context_data)


def solar7(request):
    """
    This function is used to render Solar7 view
    """
    solar7_env = sorted(SOLAR7_ENV.keys(), key=lambda item: int(item.split('.')[2]))
    solar7_env_details = SOLAR7_ENV
    mount = get_data_from_file('solar7')
    context_data = {'solar7_env': solar7_env, 'solar7_env_details': solar7_env_details,
                    'mount': mount}
    return render(request, 'env/solar7.html', context=context_data)


class EnvironmentAddView(AjaxFormMixin, FormView):
    """
    This function is used to handle System Add View
    """
    form_class = EnvironmentForm
    template_name = 'env/environment_add.html'
    success_url = reverse_lazy('env:all')

    def get_form_kwargs(self):
        context = super(EnvironmentAddView, self).get_form_kwargs()
        context['request'] = self.request
        return context

    def form_valid(self, form):
        response = super(EnvironmentAddView, self).form_valid(form)
        if self.request.is_ajax():
            post_data = dict(self.request.POST.items())
            system_id = post_data['system_id']
            environment_type = post_data['environment_type']
            environment_data_type_id = post_data['environment_data_type']
            environment_name = form.cleaned_data["environment_name"]
            creation_date = form.cleaned_data["creation_date"]

            data = {
                "environment_name": environment_name,
                "environment_type_id": environment_type,
                "creation_date": creation_date,
                "environment_data_type_id": environment_data_type_id,
                "system_id" : system_id
            }
            print(data)
            resp = post_request_secure("/api/v1/environment", data, self.request.COOKIES.get('access_token'))
            if resp.status_code == status.HTTP_200_OK:
                resp_data = json.loads(resp.text)
                resp_data["url"] = reverse_lazy('env:all')
                #self.request.session["resp_data"] = resp_data['environment_id']
                return JsonResponse(resp_data, status=resp.status_code, safe=False)
            return JsonResponse(resp.text, status=resp.status_code, safe=False)
        return response

def map_instance(request, env_id, system_id, system_element_id):
    """
    This function is used to render map instance view
    """
    form_data = {}
    if request.method == 'POST':
        if request.is_ajax():
            post_data = dict(request.POST.items())
            data = {
                    "system_element_id": post_data['system_element_id'],
                    "environment_id": post_data["environment_id"],
                    "instance_id":  post_data["instance_id"],
                    "system_id": post_data["system_id"]
                    #"system_version_id": post_data["system_version_id"]
                }
            resp = post_request_secure("/api/v1/instance_allocation", data ,  request.COOKIES.get('access_token'))
            if resp.status_code == status.HTTP_200_OK:
                resp_data = json.loads(resp.text)
                #resp_data["url"] = reverse_lazy('env:all')
                return JsonResponse(json.dumps(resp_data),safe=False)
            return JsonResponse(resp.text, status=resp.status_code, safe=False)
    else :
        resp = get_request_secure("/api/v1/mapinstance?env_id=" + env_id + "&system_id=" + system_id + "&system_element_id=" + system_element_id ,  request.COOKIES.get('access_token'))
        if resp.status_code == status.HTTP_200_OK:
            resp_data = json.loads(resp.text)
            form_data = resp_data
            
        else :
            return JsonResponse(resp.text, status=resp.status_code, safe=False)
    return render(request, 'env/map_instance.html', {'data':form_data})
