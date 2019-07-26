"""
This module is used to handle all the views related to Delivery DB App
"""
import json
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import FormView
from rest_framework import status
from esmt.api.abstract import post_request, get_request, put_request ,get_request_secure, post_request_secure, put_request_secure
from esmt.api.mixins import AjaxFormMixin
from .forms import SystemForm, SystemVersionForm, ComponentForm, ComponentVersionForm, \
    InfraTemplateForm, InstanceAddForm, InstanceUpdateForm, NetworkSetForm, hostTypeForm, hostSubForm, hostRegionForm, hostSiteForm


def host_view(request):
    """
    This function is used to handle the list of hosts View
    """
    host_type = get_request_secure("/api/v1/host_type" ,  request.COOKIES.get('access_token'))
    instances = get_request_secure("/api/v1/instance" ,  request.COOKIES.get('access_token'))
    try:
        host_list = []
        total_instances = 0
        err_msg = ""
        if host_type.status_code == status.HTTP_200_OK and \
                instances.status_code == status.HTTP_200_OK:
            host_type_data = json.loads(host_type.text)
            instance_data = json.loads(instances.text)
            instance_up_list =[ins for ins in instance_data['instances'] if ins["instance_state"].upper() == 'UP']
            total_instances = len(instance_up_list)
            for host in host_type_data["host_types"]:
                hosts = dict()
                hosts['host_id'] = host['host_type_id']
                hosts['host_name'] = host['host_name']
                instance_cnt = 0
                for instance in instance_up_list:
                    if instance['infrastructure_template']['host_type']['host_name'] == \
                            host["host_name"]:
                        instance_cnt = instance_cnt + 1
                hosts['instance_cnt'] = instance_cnt
                if instance_cnt > 0 and total_instances > 0:
                    hosts['instance_percent'] = str(
                        float("{0:.2f}".format((instance_cnt / total_instances) * 100))) + '%'
                else:
                    hosts['instance_percent'] = "0%"
                host_list.append(hosts)
        else:
            err_msg = 'Unable to get Instance details or No Instance Found'
    except Exception as e:
        print(e.__doc__)
        print(e.message)
        err_msg = 'Unable to connect to Delivery DB'
    context_data = {'hosts': host_list, 'count': total_instances, 'error': err_msg}
    return render(request, 'delivery_db/hosts.html', context=context_data)


def instance_view(request):
    """
    This function is used to render instances View
    """
    # instance_lists = get_request_secure("/api/v1/instances")
    # context_data = {"instances": json.loads(instance_lists.text)}
    return render(request, 'delivery_db/instances.html', context={})


def softwares(request):
    """
    This function is used to render softwares View
    """
    return render(request, 'delivery_db/softwares.html', {})


def systems(request):
    """
    This function is used to render systems View
    """
    # system_lists = get_request_secure("/api/v1/systems")
    # context_data = {"systems": json.loads(system_lists.text)}
    return render(request, 'delivery_db/systems.html', context={})


def infrastructure(request):
    """
    This function is used to render infrastructure View
    """
    return render(request, 'delivery_db/infrastructure.html', context={})



def network_set(request):
    """
    This function is used to render network set view

    """
    return render(request, 'delivery_db/network_set.html',context={})


def host_type(request):
    """
    This function is used to render host type view
    """
    return render(request, 'delivery_db/host_type.html',context={})


def host_subscription(request):
    """
    This function is used to render host subscription view
    """
    return render(request, 'delivery_db/host_subscription.html',context={})


def host_region(request):
    """
    This function is used to render host subscription view
    """
    return render(request, 'delivery_db/host_region.html',context={})


def host_site(request):
    """
    This function is used to render host subscription view
    """
    return render(request, 'delivery_db/host_site.html',context={})



class InstanceAddView(AjaxFormMixin, FormView):
    """
    This class is used to render release version add view and handle release add form submission
    """
    form_class = InstanceAddForm
    template_name = 'delivery_db/instance_add.html'
    success_url = reverse_lazy('delivery_db:instances')

    def get_form_kwargs(self):
        context = super(InstanceAddView, self).get_form_kwargs()
        context['request'] = self.request
        return context

    def form_valid(self, form):
        """
        This function is used to validate the Instance - form data, handle form submission
        and respond with the status
        """
        response = super(InstanceAddView, self).form_valid(form)
        # print(self.request.COOKIES['access_token'])
        if self.request.is_ajax():

            data = {
                "instance_name": form.cleaned_data["instance_name"],
                "host_instance_name": form.cleaned_data["host_instance_name"],
                "assigned_ip": form.cleaned_data["assigned_ip"],
                "instance_state": form.cleaned_data["instance_state"],
                "remarks": form.cleaned_data["remarks"],
                "creation_date": form.cleaned_data["creation_date"],
                "infra_template_id": form.cleaned_data["infra_template_id"],
                "method_creation_type_id": form.cleaned_data["method_creation_type_id"]
            }

            post_data = dict(self.request.POST.items())
            instance_disk_list = []
            # Get All the instance disk details
            for inst_disk in range(0, 50):
                instance_disk = {}
                try:
                    instance_disk["disk_type_id"] = post_data["disk_type_id-" + str(inst_disk)]
                    instance_disk["disk_size"] = post_data["disk_size-" + str(inst_disk)]
                    instance_disk["disk_size_type"] = post_data["disk_size_type-" + str(inst_disk)]
                    instance_disk_list.append(instance_disk)
                except:
                    break
            data["instance_disks"] = instance_disk_list
            resp = post_request_secure("/api/v1/instance", data, self.request.COOKIES.get('access_token'))
            if resp.status_code == status.HTTP_200_OK:
                resp_data = json.loads(resp.text)
                return JsonResponse(json.dumps(resp_data), status=resp.status_code, safe=False)
            return JsonResponse(resp.text, status=resp.status_code, safe=False)
        return response


def instance_update_view(request, instance_id):
    """
    This function is used to render Instance update view and handle instance update form submission
    """

    if request.method == 'POST':
        request.POST = request.POST.copy()
        request.POST['request'] = request.COOKIES.get('access_token')     
        form = InstanceUpdateForm(request.POST)
        if form.is_valid():
            if request.is_ajax():
                instance_state = form.cleaned_data["instance_state"]
                infra_template_id = form.cleaned_data["infra_template_id"]
                remarks = form.cleaned_data["remarks"]

                data = {
                    "instance_id": instance_id,
                    "remarks": remarks
                }
                if instance_state != '':
                    data["instance_state"] = instance_state
                if infra_template_id != '':
                    data["infra_template_id"] = infra_template_id
                resp = put_request_secure("/api/v1/instance", data ,  request.COOKIES.get('access_token'))
                if resp.status_code == status.HTTP_200_OK:
                    resp_data = json.loads(resp.text)
                    resp_data["url"] = reverse_lazy('delivery_db:instances')
                    return JsonResponse(resp_data, status=resp.status_code, safe=False)
                return JsonResponse(resp.text, status=resp.status_code, safe=False)

    else:
        resp = get_request_secure("/api/v1/instance?instance_id=" + instance_id ,  request.COOKIES.get('access_token'))
        form_data = {}
        if resp.status_code == status.HTTP_200_OK:
            resp_data = json.loads(resp.text)
            inst_resp_data = resp_data["instances"][0]
            print(inst_resp_data)
            form_data = {"instance_name": inst_resp_data["instance_name"],
                         "instance_state": inst_resp_data["instance_state"],
                         "infra_template_id":
                             inst_resp_data["infrastructure_template"]["infra_template_id"],
                         "remarks":  inst_resp_data["remarks"]
                        }

        form = InstanceUpdateForm(initial=form_data ,request=request)
    return render(request, 'delivery_db/instance_update.html', {'form': form})


class SystemView(AjaxFormMixin, FormView):
    """
    This function is used to handle System Add View
    """
    form_class = SystemForm
    template_name = 'delivery_db/system_add.html'
    success_url = reverse_lazy('delivery_db:system_version_add')

    def get_form_kwargs(self):
        context = super(SystemView, self).get_form_kwargs()
        context['request'] = self.request
        return context

    def form_valid(self, form):
        response = super(SystemView, self).form_valid(form)
        if self.request.is_ajax():
            system_name = form.cleaned_data["system_name"]
            system_short_name = form.cleaned_data["system_short_name"]
            creation_date = form.cleaned_data["creation_date"]
            system_network_set_id = form.cleaned_data["system_network_set_id"]
            data = {
                "system_name": system_name,
                "system_short_name": system_short_name,
                "creation_date": creation_date,
                "system_network_set_id": system_network_set_id,
            }
            resp = post_request_secure("/api/v1/system", data, self.request.COOKIES.get('access_token'))
            if resp.status_code == status.HTTP_200_OK:
                resp_data = json.loads(resp.text)
                resp_data["url"] = reverse_lazy('delivery_db:system_version_add')
                self.request.session["resp_data"] = resp_data['system_id']
                return JsonResponse(resp_data, status=resp.status_code, safe=False)
            return JsonResponse(resp.text, status=resp.status_code, safe=False)
        return response


def save_system_element_component(system_version_id, sys_element_id, post_data, index, resp_data , request):
    """
    This function is used to save the system element components for the system_element and system version
    """
    # print('in save_system_element_component')
    # print(request)
    for key, value in post_data.items():
        field = key.split("-")
        if field[0] == "compVer" and field[1] == index:
            component_version_id = post_data["compVer-" + str(index) + "-" + str(field[2])]
            try:
                compDeployementOrder = post_data["compDeployementOrder-" + str(index) + "-" + str(field[2])]
            except:
                compDeployementOrder = 0
            system_element_component_data = {
                "system_element_id": sys_element_id,
                "system_version_id": system_version_id,
                "component_version_id": component_version_id,
                "install_order": compDeployementOrder
            }
            # print(system_element_component_data)
            # print(request.COOKIES.get('access_token'))
            resp = post_request_secure("/api/v1/system_element_component", system_element_component_data , request.COOKIES.get('access_token'))
            if resp.status_code == status.HTTP_200_OK:
                returned_data = json.loads(resp.text)
                resp_data["system_element_component_id-" + str(index) + "-" + str(field[2])] = \
                    str(returned_data["system_element_component_id"])
            else:
                returned_data = json.loads(resp.text)
                message = returned_data["message"]
                resp_data["message" + str(index) + "-" + str(field[2])] = message


def validate_save_system_element(system_id, system_version_id, post_data, response_data ,request):
    """
    This function is used to loop through the POSTed data and save system_element and
    """
    for post_key, post_value in post_data.items():
        # print(post_key + ":" + post_value)
        form_field_name = post_key.split("-")
        # print(form_field_name)
        if form_field_name[0] == "system_element_id":
            # Save the system element if it is a newly created one
            if post_data["system_element_id-" + form_field_name[1]] == '-1':
                system_element_data = {
                    "system_id": system_id,
                    "system_element_name": post_data["system_element_name-" +
                                                     form_field_name[1]],
                    "system_element_short_name": post_data["system_element_short_name-" +
                                                           form_field_name[1]],
                    "system_element_type_id": post_data["system_element_type_id-" +
                                                        form_field_name[1]],
                }
                # print(system_element_data)
                resp = post_request_secure("/api/v1/system_element", system_element_data , request.COOKIES.get('access_token'))
                if resp.status_code == status.HTTP_200_OK:
                    returned_data = json.loads(resp.text)
                    system_element_id = returned_data["system_element_id"]
                    response_data["system_element_id-" + form_field_name[1]] = system_element_id
                    save_system_element_component(system_version_id, system_element_id, post_data,
                                                  form_field_name[1], response_data , request)
                else:
                    returned_data = json.loads(resp.text)
                    response_data["system_element_message-" + form_field_name[1]] =\
                        returned_data["message"]
            else:
                # Get the system element id if the system element is already present
                system_element_id = post_data["system_element_id-" + form_field_name[1]]
                save_system_element_component(system_version_id, system_element_id, post_data,
                                              form_field_name[1], response_data , request )


class SystemVersionView(AjaxFormMixin, FormView):
    """
    This function is used to handle System version Add View
    """
    form_class = SystemVersionForm
    template_name = 'delivery_db/system_version_add.html'
    success_url = '/form-success/'

    def get_context_data(self, **kwargs):
        context = super(SystemVersionView, self).get_context_data(**kwargs)
        context['resp_data'] = self.request.session.pop('resp_data', "")
        return context

    def get_form_kwargs(self):
        context = super(SystemVersionView, self).get_form_kwargs()
        # context['resp_data'] = self.request.session.pop('resp_data', "")
        context['request'] = self.request
        return context

    def form_valid(self, form):
        response = super(SystemVersionView, self).form_valid(form)
        if self.request.is_ajax():
            system_id = form.cleaned_data["system_name"]

            # Save System version details
            data = {
                "system_id": form.cleaned_data["system_name"],
                "system_version_name": form.cleaned_data["system_version_name"],
                "creation_date": form.cleaned_data["creation_date"]
            }
            response_data = dict()
            print(data)   
            resp = post_request_secure("/api/v1/system_version", data, self.request.COOKIES.get('access_token'))
            if resp.status_code == status.HTTP_200_OK:
                post_data = dict(self.request.POST.items())
                returned_data = json.loads(resp.text)
                system_version_id = returned_data["system_version_id"]
                validate_save_system_element(system_id, system_version_id, post_data, response_data , self.request)
                response_data["system_version_id"] = str(system_version_id)
            else:
                returned_data = json.loads(resp.text)
                response_data["message"] = returned_data["message"]
            return JsonResponse(json.dumps(response_data), status=resp.status_code, safe=False)
        else:
            return response


class ComponentView(AjaxFormMixin, FormView):
    """
    This function is used to handle Component Add View
    """
    form_class = ComponentForm
    template_name = 'delivery_db/component_add.html'
    success_url = reverse_lazy('delivery_db:component_version_add')

    def get_form_kwargs(self):
        context = super(ComponentView, self).get_form_kwargs()
        # context['resp_data'] = self.request.session.pop('resp_data', "")
        context['request'] = self.request
        return context

    def form_valid(self, form):
        response = super(ComponentView, self).form_valid(form)
        if self.request.is_ajax():
            component_name = form.cleaned_data["component_name"]
            component_short_name = form.cleaned_data["component_short_name"]
            component_type_description = form.cleaned_data["component_type_description"]
            creation_date = form.cleaned_data["creation_date"]
            linked_ci_flag = form.cleaned_data["linked_ci_flag"]
            deployment_type_id = form.cleaned_data["deployment_type"]
            data = {
                "component_name": component_name,
                "component_short_name": component_short_name,
                "creation_date": creation_date,
                "component_type_description": component_type_description,
                "linked_ci_flag": linked_ci_flag,
                "deployment_type_id": deployment_type_id
            }
            resp = post_request_secure("/api/v1/component", data, self.request.COOKIES.get('access_token'))
            if resp.status_code == status.HTTP_200_OK:
                resp_data = json.loads(resp.text)
                resp_data["url"] = reverse_lazy('delivery_db:component_version_add')
                self.request.session["resp_data"] = resp_data['component_id']
                return JsonResponse(resp_data, status=resp.status_code, safe=False)
            return JsonResponse(resp.text, status=resp.status_code, safe=False)
        return response


class ComponentVersionView(AjaxFormMixin, FormView):
    """
    This function is used to handle Component Version Add View
    """
    form_class = ComponentVersionForm
    template_name = 'delivery_db/component_version_add.html'
    success_url = reverse_lazy('delivery_db:components')

    def get_context_data(self, **kwargs):
        context = super(ComponentVersionView, self).get_context_data(**kwargs)
        context['resp_data'] = self.request.session.pop('resp_data', "")
        return context

    def get_form_kwargs(self):
        context = super(ComponentVersionView, self).get_form_kwargs()
        context['request'] = self.request
        return context

    def form_valid(self, form):
        response = super(ComponentVersionView, self).form_valid(form)
        if self.request.is_ajax():
            component_version_name = form.cleaned_data["component_version_name"]
            artefact_store_url = form.cleaned_data["artefact_store_url"]
            source_code_repository_url = form.cleaned_data["source_code_repository_url"]
            source_tag_reference = form.cleaned_data["source_tag_reference"]
            creation_date = form.cleaned_data["creation_date"]
            artefact_store_type_desc = form.cleaned_data["artefact_store_type_desc"]
            component_name = form.cleaned_data["component_name"]
            data = {
                "component_name": component_name,
                "component_version_name": component_version_name,
                "stable_flag": 1,
                "artefact_store_url": artefact_store_url,
                "source_code_repository_url": source_code_repository_url,
                "source_tag_reference": source_tag_reference,
                "creation_date": creation_date,
                "artefact_store_type_desc": artefact_store_type_desc
            }
            resp = post_request_secure("/api/v1/component_version", data, self.request.COOKIES.get('access_token'))
            return JsonResponse(resp.text, status=resp.status_code, safe=False)
        return response


def components(request):
    """
    This function is used to render components View
    """
    return render(request, 'delivery_db/components.html', {})


def system_component(request):
    """
    This function is used to handle system component View
    """
    if request.method == "POST":
        post_data = dict(request.POST.items())
        system_version_id = post_data['system_version']
        component_versions = []
        # Get All the component version details
        for key, val in post_data.items():
            if 'compVer' in key:
                component_versions.append(val)
        for component in component_versions:
            component_version_id = component
            data = {
                "system_version_id": system_version_id,
                "component_version_id": component_version_id
            }
            resp = post_request_secure("/api/v1/system_component", data ,  request.COOKIES.get('access_token'))
        return JsonResponse(resp.text, status=resp.status_code, safe=False)

    return render(request, 'delivery_db/system_component.html', {})


class InfraTemplateView(AjaxFormMixin, FormView):
    """
    This function is used to handle Infrastructure Add View
    """
    form_class = InfraTemplateForm
    template_name = 'delivery_db/infra_template_add.html'
    success_url = reverse_lazy('delivery_db:infrastructure')


    def get_form_kwargs(self):
        context = super(InfraTemplateView, self).get_form_kwargs()
        context['request'] = self.request
        return context

    def form_valid(self, form):
        response = super(InfraTemplateView, self).form_valid(form)
        if self.request.is_ajax():
            post_data = dict(self.request.POST.items())
            print(post_data)
            infra_template_name = form.cleaned_data["infra_template_name"]
            host_template_description = form.cleaned_data["host_template_description"]
            infrastructure_type_id = form.cleaned_data["infrastructure_type_id"]
            if infrastructure_type_id != '2':
                cpu = post_data["cpu"]
                memory_size = post_data["memory_size"]
                max_no_disk = post_data["max_no_disk"]
            host_type_id = form.cleaned_data["host_type_id"]

            data = {
                "infra_template_name": infra_template_name,
                "host_template_description": host_template_description,
                "host_type_id": host_type_id,
                "infrastructure_type_id" : infrastructure_type_id
            }
            if infrastructure_type_id != '2':
                data["cpu"] = cpu
                data["memory_size"] = memory_size
                data["max_no_disk"] = max_no_disk

            resp = post_request_secure("/api/v1/infrastructure_template", data, self.request.COOKIES.get('access_token') )
            if resp.status_code == status.HTTP_200_OK:
                resp_data = json.loads(resp.text)
                resp_data["url"] = reverse_lazy('delivery_db:infrastructure')
                return JsonResponse(resp_data, status=resp.status_code, safe=False)
            return JsonResponse(resp.text, status=resp.status_code, safe=False)
        return response



class NetworkSetView(AjaxFormMixin, FormView):
        """
        This function is used to handle Network Set Add View
        """
        form_class = NetworkSetForm
        template_name = 'delivery_db/network_set_add.html'
        success_url = reverse_lazy('delivery_db:network_set')

        def form_valid(self, form):
            response = super(NetworkSetView, self).form_valid(form)
            if self.request.is_ajax():
                post_data = dict(self.request.POST.items())
                network_set_name = form.cleaned_data["network_set_name"]
                host_subscription_id = post_data["host_subscription"]
                host_site_id = post_data["host_site"]
                environment_type_id = post_data["environment_type"]
                system_element_type_id = post_data["system_element_type"]
                subnet = form.cleaned_data["subnet"]
                ip_range_start = form.cleaned_data["ip_start"]
                ip_range_end = form.cleaned_data["ip_end"]
                
                data = {
                    "network_set_name": network_set_name,
                    "host_subscription_id": host_subscription_id,
                    "host_site_id": host_site_id,
                    "environment_type_id": environment_type_id,
                    "system_element_type_id": system_element_type_id,
                    "ip_range_start": ip_range_start,
                    "ip_range_end": ip_range_end,
                    "subnet": subnet 
                    

                }
                resp = post_request_secure("/api/v1/network_set", data, self.request.COOKIES.get('access_token'))
                if resp.status_code == status.HTTP_200_OK:
                    resp_data = json.loads(resp.text)
                    resp_data["url"] = reverse_lazy('delivery_db:network_set')
                    return JsonResponse(resp_data, status=resp.status_code, safe=False)
                return JsonResponse(resp.text, status=resp.status_code, safe=False)
            return response


class hostTypeView(AjaxFormMixin,FormView):
    """
    This function is used to handle host Type add
    """
    form_class = hostTypeForm
    template_name = 'delivery_db/host_type_add.html'
    success_url = reverse_lazy('delivery_db:host_type')

    def form_valid(self,form):
        response = super(hostTypeView, self).form_valid(form)
        if self.request.is_ajax():
            host_name = form.cleaned_data["host_name"]
            
            data = {
             "host_name" : host_name
             
            }
            resp = post_request_secure("/api/v1/host_type",data, self.request.COOKIES.get('access_token'))
            if resp.status_code == status.HTTP_200_OK:
                resp_data = json.loads(resp.text)
                resp_data["url"] = reverse_lazy('delivery_db:host_type')
                return JsonResponse(resp_data, status=resp.status_code, safe=False)
            return JsonResponse(resp.text, status=resp.status_code, safe=False)
        return response



class hostSubView(AjaxFormMixin,FormView):
    """
    This function is used to handle Host subscription add
    """
    form_class = hostSubForm
    template_name = 'delivery_db/host_subscription_add.html'
    success_url = reverse_lazy('delivery_db:host_subscription')

    def form_valid(self,form):
        response =  super(hostSubView, self).form_valid(form)
        if self.request.is_ajax():
            post_data = dict(self.request.POST.items())
            host_subscription_description = form.cleaned_data["host_subscription_name"]
            host_region = post_data["host_region"]
            system_network_set = post_data["system_network_set"]
            environment_sub = post_data["environment_sub"]
            environment_type = post_data["environment_type"]
            host_subscription_key = form.cleaned_data["host_subscription_key"]

            data = {
                "host_subscription_description" : host_subscription_description,
                "host_region_id" : host_region,
                "system_network_set_id" : system_network_set,
                "environment_sub_id" : environment_sub,
                "environment_type_id" : environment_type,
                "host_subscription_key" : host_subscription_key
                 }
            resp = post_request_secure("/api/v1/host_subscription", data, self.request.COOKIES.get('access_token'))
            if resp.status_code == status.HTTP_200_OK:
                resp_data = json.loads(resp.text)
                resp_data["url"] = reverse_lazy('delivery_db:host_subscription')
                return JsonResponse(resp_data, status=resp.status_code, safe=False)
            return JsonResponse(resp.text, status=resp.status_code, safe=False)
        return response


class hostRegionView(AjaxFormMixin,FormView):
    """
    This function is used to handle host Region add View
    """
    form_class = hostRegionForm
    template_name = 'delivery_db/host_region_add.html'
    success_url = reverse_lazy('delivery_db:host_region')


    def get_form_kwargs(self):
        context = super(hostRegionView, self).get_form_kwargs()
        context['request'] = self.request
        return context

    def form_valid(self,form):
        response = super(hostRegionView, self).form_valid(form)
        if self.request.is_ajax():
            host_region_name = form.cleaned_data["host_region_name"]
            host_region_description = form.cleaned_data["host_region_description"]
            host_type_id = form.cleaned_data["host_type"]

            data = {
             "host_region_name": host_region_name,
             "host_region_description": host_region_description,
             "host_type_id": host_type_id
            }
            resp = post_request_secure("/api/v1/host_region",data, self.request.COOKIES.get('access_token'))
            if resp.status_code == status.HTTP_200_OK:
                resp_data = json.loads(resp.text)
                resp_data["url"] = reverse_lazy('delivery_db:host_region')
                return JsonResponse(resp_data, status=resp.status_code, safe=False)
            return JsonResponse(resp.text, status=resp.status_code, safe=False)
        return response


class hostSiteView(AjaxFormMixin,FormView):
    """
    This function is used to handle host Region add View
    """
    form_class = hostSiteForm
    template_name = 'delivery_db/host_site_add.html'
    success_url = reverse_lazy('delivery_db:host_site')

    def get_form_kwargs(self):
        context = super(hostSiteView, self).get_form_kwargs()
        context['request'] = self.request
        return context

    def form_valid(self,form):
        response = super(hostSiteView, self).form_valid(form)
        if self.request.is_ajax():
            host_site_name = form.cleaned_data["host_site_name"]
            host_site_description = form.cleaned_data["host_site_description"]
            host_region_id = form.cleaned_data["host_region"]

            data = {
             "host_site_name": host_site_name,
             "host_site_description": host_site_description,
             "host_region_id": host_region_id
            }
            resp = post_request_secure("/api/v1/host_site",data, self.request.COOKIES.get('access_token'))
            if resp.status_code == status.HTTP_200_OK:
                resp_data = json.loads(resp.text)
                resp_data["url"] = reverse_lazy('delivery_db:host_site')
                return JsonResponse(resp_data, status=resp.status_code, safe=False)
            return JsonResponse(resp.text, status=resp.status_code, safe=False)
        return response
