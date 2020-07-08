from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.models import Permission
from .models import *
# Register your models here.


admin.site.register(projectWorker)
admin.site.register(project)
admin.site.register(leadContact)

class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'inactive')
    list_display_links = list_display
    list_filter = ('name', 'inactive')
admin.site.register(Client, ClientAdmin)