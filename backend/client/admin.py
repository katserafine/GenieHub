from django.contrib import admin
from .models import client, projectWorker, project, leadContact

admin.site.register(client)
admin.site.register(projectWorker)
admin.site.register(project)
admin.site.register(leadContact)