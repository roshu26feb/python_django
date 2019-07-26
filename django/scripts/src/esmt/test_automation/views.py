"""
Author: Yogaraja Gopal
This module is used to handle view for test_automation app
"""
import json
import datetime
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import FormView
from rest_framework import status


def test_runs(request):
    """
    This function is used to render releases view
    """
    return render(request, 'test_automation/test_runs.html', {})

'''
class CreateTestRunsView(AjaxFormMixin, FormView):
    """
    This class is used to render release add view and handle release add form submission
    """
    form_class = ReleaseAddForm
    template_name = 'releases/release_add.html'
    success_url = reverse_lazy('releases:release_version_add')

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
            resp = post_request_secure("/api/v1/release", data)
            if resp.status_code == status.HTTP_200_OK:
                resp_data = json.loads(resp.text)
                resp_data["url"] = reverse_lazy('releases:release_version_add')
                self.request.session["resp_data"] = resp_data['release_id']
                self.request.session["rel_name"] = release_name
                return JsonResponse(resp_data, status=resp.status_code, safe=False)
            return JsonResponse(resp.text, status=resp.status_code, safe=False)
        return response


class CreateTestSetView(AjaxFormMixin, FormView):
    """
    This class is used to render release add view and handle release add form submission
    """
    form_class = ReleaseAddForm
    template_name = 'test_automation/test_set_add.html'
    success_url = reverse_lazy('test_automation:release_version_add')

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
            resp = post_request_secure("/api/v1/release", data)
            if resp.status_code == status.HTTP_200_OK:
                resp_data = json.loads(resp.text)
                resp_data["url"] = reverse_lazy('releases:release_version_add')
                self.request.session["resp_data"] = resp_data['release_id']
                self.request.session["rel_name"] = release_name
                return JsonResponse(resp_data, status=resp.status_code, safe=False)
            return JsonResponse(resp.text, status=resp.status_code, safe=False)
        return response
'''
