from django.http import HttpResponse
from django.shortcuts import render
from client.models import project
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django import http
from django.conf import settings
from django.template import engines
import requests


def catchall_dev(request, upstream='http://localhost:3000'):
    upstream_url = upstream + request.path
    response = requests.get(upstream_url)
    content = engines['django'].from_string(response.text).render()
    return http.HttpResponse(content)

catchall_prod = TemplateView.as_view(template_name='index.html')

catchall = catchall_dev if settings.DEBUG else catchall_prod


def index(request):
    num_projects = User.objects.all().count()

    context = {
        'num_projects' : num_projects,
    } 

    return render(request, 'index.html', context=context)


def homepage(request):
    num_projects = User.objects.all().count()

    context = {
        'num_projects' : num_projects,
    } 

    return render(request, 'homepage.html', context=context)
