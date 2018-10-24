from django.contrib import admin
from .models import *


class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('progress_time', 'progress_start')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Question)
