from django.contrib import admin
from .models import Events, SubEvents, Status

admin.site.register(Events)
admin.site.register(SubEvents)
admin.site.register(Status)