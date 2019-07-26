"""
Author: Yogaraja Gopal
This module is used to handle view for esmt_base app
"""
import json
from django.shortcuts import render, redirect
from esmt.api.abstract import post_request, get_request, put_request
from rest_framework import status
from django.http import JsonResponse
from urllib import parse


# Create your views here.
def index(request):
    """
    This function is used to handle base View of ESMT
    """
    get_data = dict(request.GET.items())
    if(get_data):
        msg_data = get_data['message']
    else:
        msg_data = ''
    return render(request, 'base/esmt.html', {'msg':msg_data})

def login(request):
    """
    This function is used to handle login View of ESMT
    """
    if request.method == 'POST':
        post_data = dict(request.POST.items())
        data = {
                "userName": post_data['userName'],
                "password": post_data["password"]
            }
        resp = post_request("/api/v2/auth/token", data)
        resp_data = json.loads(resp.text)
        if resp.status_code == status.HTTP_200_OK :                      
            response = redirect('/') 
            response.set_cookie("access_token", value=parse.quote(str(resp_data['access_token'])))
            response.set_cookie("refresh_token", value=parse.quote(str(resp_data['refresh_token'])))
         
            return response
        else:
            response = render(request, 'base/login.html', {'message' : resp_data["message"] })
            return response
        return JsonResponse(resp.text, status=resp.status_code, safe=False)
    else:
        return render(request, 'base/login.html', {})
    
def logout(request):
    ''' logout user '''
    response = redirect('/login')
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response