"""
Author: Yogaraja Gopal
This module is used to handle view for release app
"""
import json
import datetime
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import FormView
from rest_framework import status
from esmt.api.abstract import post_request, post_request_secure
from esmt.api.mixins import AjaxFormMixin
from .forms import ReleaseAddForm, ReleaseVersionAddForm, routeToLiveForm


def releases(request):
    """
    This function is used to render releases view
    """
    return render(request, 'release/releases.html', {})


class ReleaseAddView(AjaxFormMixin, FormView):
    """
    This class is used to render release add view and handle release add form submission
    """
    form_class = ReleaseAddForm
    template_name = 'release/release_add.html'
    success_url = reverse_lazy('release:release_version_add')

    def form_valid(self, form):
        """
        This function is used to validate the release add - form data, handle form submission and
        respond with the status
        """
        response = super(ReleaseAddView, self).form_valid(form)
        if self.request.is_ajax():
            release_name = form.cleaned_data["release_name"]
            release_owner = form.cleaned_data["release_owner"]
            release_summary = form.cleaned_data["release_summary"]
            data = {
                "release_name": release_name,
                "release_owner": release_owner,
                "release_summary": release_summary
            }
            resp = post_request_secure("/api/v1/release", data, self.request.COOKIES.get('access_token'))
            if resp.status_code == status.HTTP_200_OK:
                resp_data = json.loads(resp.text)
                resp_data["url"] = reverse_lazy('release:release_version_add')
                self.request.session["resp_data"] = resp_data['release_id']
                self.request.session["rel_name"] = resp_data['release_id']
                return JsonResponse(resp_data, status=resp.status_code, safe=False)
            return JsonResponse(resp.text, status=resp.status_code, safe=False)
        return response


class ReleaseVersionAddView(AjaxFormMixin, FormView):
    """
    This class is used to render release version add view and handle release add form submission
    """
    form_class = ReleaseVersionAddForm
    template_name = 'release/release_version_add.html'
    success_url = reverse_lazy('release:release_version_add')

    def get_form_kwargs(self):
      
        kwargs = super(ReleaseVersionAddView, self).get_form_kwargs()
        kwargs['rel_name'] = self.request.session.pop('rel_name', '')
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        """
        This function is used to pass addition context data to template
        """
        context = super(ReleaseVersionAddView, self).get_context_data(**kwargs)
        context['resp_data'] = self.request.session.pop('resp_data', "")
        return context

    def form_valid(self, form):
        """
        This function is used to validate the Release version - form data, handle form submission
        and respond with the status
        """
        response = super(ReleaseVersionAddView, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                "release_id": form.cleaned_data["release_name"],
                "release_version_name": form.cleaned_data["release_version_name"],
                "creation_date": datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S"),
                "target_release_date": form.cleaned_data["release_target_date"] + " 12:00:00",
                "release_version_status_id": form.cleaned_data["release_version_status"],
                "remarks": form.cleaned_data["remarks"],
            }

            post_data = dict(self.request.POST.items())
            release_items = []
            # Get All the component version details
            for rel_item in range(0, 50):
                release_item = {}
                try:
                    release_item["system_version_id"] = \
                        post_data["system_version_id-" + str(rel_item)]
                    release_item["release_note_url"] = \
                        post_data["release_note_url-" + str(rel_item)]
                    release_items.append(release_item)
                except:
                    break
            data["release_items"] = release_items

            resp = post_request_secure("/api/v1/release_version", data, self.request.COOKIES.get('access_token'))
            if resp.status_code == status.HTTP_200_OK:
                resp_data = json.loads(resp.text)
                return JsonResponse(json.dumps(resp_data), status=resp.status_code, safe=False)
            return JsonResponse(resp.text, status=resp.status_code, safe=False)
        return response


class RouteToLiveView(AjaxFormMixin, FormView):
    """
    This function is used to render RTL view
    """
    form_class = routeToLiveForm
    template_name = 'release/rtl.html'
    success_url = reverse_lazy('release:rtl')

    def get_form_kwargs(self):
        context = super(RouteToLiveView, self).get_form_kwargs()
        context['request'] = self.request
        return context

    #return render(request, 'release/rtl.html', {})


def manage_rtl(request):
    """
    This function is used to render Manage RTL view
    """
    if request.method == 'POST':
        if request.is_ajax():
            post_data = dict(request.POST.items())
            print(post_data)
            data = {
                "release_id": post_data["release_id"],
                "system_id": post_data["system_id"]
            }
            response_data = {}
            rtl_id = []
            message = []
            status_code = status.HTTP_400_BAD_REQUEST
            for form_key, form_value in post_data.items():
                env_use = form_key.split("-")
                if env_use[0] == "environment_use_id":
                    data["environment_use_id"] = form_value
                    data["environment_id"] = post_data.get("environment_id-" + env_use[1], 'null')
                    data["route_to_live_order"] = post_data.get("order-" + env_use[1], 'null') 
                    data["critical"] = post_data.get("critical-" + env_use[1], False) 
                    print(data)
                    resp = post_request_secure("/api/v1/route_to_live", data ,  request.COOKIES.get('access_token'))
                    resp_data = json.loads(resp.text)
                    if resp.status_code == status.HTTP_200_OK:
                        rtl_id.append(resp_data["route_to_live_id"])
                        status_code = status.HTTP_200_OK
                    else:
                        message.append(resp_data["message"])
            response_data["route_to_live"] = rtl_id
            response_data["message"] = message
            return JsonResponse(response_data, status=status_code, safe=False)
    return render(request, 'release/manage_rtl.html', {})
