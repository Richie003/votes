from django.contrib import admin
from .models import *
# Register your models here.

class RoleAdmin(admin.ModelAdmin):
    list_display = [
        'role',
    ]

class ElectionAdmin(admin.ModelAdmin):
    list_display = [
        "role",
        "start_date",
        "end_date",
    ]

class CandidateAdmin(admin.ModelAdmin):
    list_display = [
        "role",
        "bio",
        "added"
    ]

class VoteTableAdmin(admin.ModelAdmin):
    list_display = [
        "voted_by",
        "role_name",
        "voted"
    ]


class VoteCheckAdmin(admin.ModelAdmin):
    list_display = [
        "role",
    ]

admin.site.register(Role, RoleAdmin)
admin.site.register(Election, ElectionAdmin)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(VoteTable, VoteTableAdmin)
admin.site.register(VoteCheck, VoteCheckAdmin)