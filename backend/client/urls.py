from django.conf.urls import *
import client.views
from .api import ClientViewSet
from rest_framework import routers

router = routers.DefaultRouter() 

router.register('api/clients', ClientViewSet, 'clients')

urlpatterns = router.urls



#urlpatterns = [
#    url(
#        regex="^manager_dashboard/clients/?$",
#        view=client.views.manager_client_dashboard,
#        name='manager_dashboard_clients'
#            ),
#    url(
#        regex ='^api/clients/?$',
#        view=client.views.client_list,
#        name="client_list"
#    ),
#]