from django.contrib import admin
from .models import GroupProfile

class GroupProfileInline(admin.StackedInline):
    model = GroupProfile
    extra = 0

from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin

class GroupAdmin(BaseGroupAdmin):
    inlines = [GroupProfileInline]

admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
