from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse, Http404, HttpResponse
from .models import Client
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from logging import getLogger
from rest_framework.request import Request
from rest_framework.renderers import JSONRenderer
from django.core import serializers


logger = getLogger("client.views")

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)



# base view for this application
#Client data for MANAGER users, used by ManagerDashboard named files
@permission_required('clients.view_client_dashboard', raise_exception=True)
def manager_client_dashboard(request):
    logger.debug('client_dashboard')
    
    # Only allow super users to access this page
    if not request.user.is_superuser:
        return HttpResponse(status=404)

    # TODO
    clients = Client.objects.filter(inactive=False)

    return JsonResponse({"clients": clients})





##  Holder function for api for client information, add delete/modify

@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def client_list(request):

    if request.method == 'GET':
        #create an array to pass client model to 
        data = []

        #read in client data (name)
        data = Client.objects.all()

        #serialize using model serializer
        serializer = ClientSerializer(data, context = {'request' : request}, many=True)

        #this returns a basic array NOT JSON
        return Response(serializer.data)

        
    elif request.method == 'POST':
        serializer = ClientSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return JSONResponse(serializer.errors, status=400)