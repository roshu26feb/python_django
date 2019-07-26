"""
This modules contains mixins used in Forms and Views
"""
import datetime
import json
from django import forms
from django.contrib.admin import widgets
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .abstract import get_request ,get_request_secure


class AjaxFormMixin(object):
    """
    This class is used to handle Ajax form Errors
    """
    def form_invalid(self, form):
        """
        This method is used to handle AJAX request form Errors
        """
        response = super(AjaxFormMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        return response


class CreationDateMixin(forms.Form):
    """
    This class is used to handle Creation of DateTime Widgets
    """
    def __init__(self, *args, **kwargs):
        super(CreationDateMixin, self).__init__(*args, **kwargs)
        self.fields['creation_date'] = forms.SplitDateTimeField(
            widget=widgets.AdminSplitDateTime(),
            initial=datetime.datetime.today())

    def clean_creation_date(self):
        """
        This method is used to clean the creation date to a particular format
        """
        data = self.cleaned_data['creation_date']
        data = datetime.datetime.strftime(data, '%d/%m/%y %H:%M:%S')
        return data


class QueryDeliveryDb(APIView):
    """
    This class is used to Query Delivery DB and return the response
    """
    url = None

    def get(self, request):
        """
        This method handles the get request
        """
        resp = get_request(self.url)
        try:
            if resp.status_code == status.HTTP_200_OK:
                return Response(json.loads(resp.text))
            return Response({"error": "Failed to get response"}, status=resp.status_code)
        except:
            return Response({"error": "error"}, status=resp["status_code"])


class GetChoiceListMixin:
    """
    This class is used to Query Delivery DB and return the response
    """
    url_param = None
    choice_key = None
    choice_value = None
    parent_element = None
    include_select = True
    access_token = None

    def get_choices(self):
        """
        This method is used to get list of Releases from Delivery DB API
        """
        
        if self.include_select:
            obj_list = [('', '--Select--')]
        else:
            obj_list = []
        try:
           
            response = get_request_secure("/api/v1/" + self.url_param , self.access_token)
            response_data = json.loads(response.text)
            if response.status_code == status.HTTP_200_OK:
                for data in response_data[self.parent_element]:
                    obj = (data[self.choice_key], data[self.choice_value].strip())
                    obj_list.append(obj)
            else:
                obj_list = [('-1', 'Error : Unable to get ' + self.url_param.replace('_', ' '))]
                obj_list.sort(key=lambda tup: tup[1].upper())
        except:
            obj_list = [('-1', 'Error : Unable to get ' + self.url_param.replace('_', ' '))]
        return obj_list


class GetChoiceDictMixin:
    """
    This class is used to Query Delivery DB and return the response
    """
    url_param = None
    choice_key = None
    choice_value = None
    parent_element = None
    access_token = None

    def get_choices(self):
        """
        This method is used to get list of Releases from Delivery DB API
        """
        obj_list = []
        try:
            response = get_request_secure("/api/v1/" + self.url_param , self.access_token)
            response_data = json.loads(response.text)
            if response.status_code == status.HTTP_200_OK:
                for data in response_data[self.parent_element]:
                    obj = dict()
                    obj['key'] = data[self.choice_key]
                    obj['value'] = data[self.choice_value].strip()
                    obj_list.append(obj)
            else:
                obj_list = [('-1', 'Error : Unable to get ' + self.url_param.replace('_', ' '))]
                obj_list.sort(key=lambda tup: tup[1].upper())
        except:
            obj_list = [('-1', 'Error : Unable to get ' + self.url_param.replace('_', ' '))]
        return obj_list
