from django.contrib import admin

from .models import Trip, Waypoint


@admin.register(Waypoint)
class WaypointAdmin(admin.ModelAdmin):
    list_display = ('lat', 'lng', 'order', 'trip')


class WaypointInlineAdmin(admin.TabularInline):

    model = Waypoint


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'modified')
    inlines = [WaypointInlineAdmin]

