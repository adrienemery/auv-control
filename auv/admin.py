from django.contrib import admin

from .models import AUV


@admin.register(AUV)
class AUVAdmin(admin.ModelAdmin):
    pass
