from django.contrib import admin
from django.contrib.auth.views import LoginView
from forms.admin import CustomAuthenticationForm
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import *

admin.site.site_header = ''
admin.site.index_title = ''


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('reg_no', 'email', 'admin', 'first_name', 'last_name',)
    list_filter = ('admin',)
    fieldsets = (
        (None, {'fields': ('reg_no', 'email', 'password', 'first_name', 'last_name',)}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('reg_no', 'email', 'password1', 'password2', 'first_name', 'last_name',)}
         ),
    )
    search_fields = ('reg_no', 'email', 'first_name', 'last_name',)
    ordering = ('reg_no', 'email', 'first_name', 'last_name',)
    filter_horizontal = ()

class FacultyAdmin(admin.ModelAdmin):
    list_display = [
        'faculty_name',
    ]

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'admin/login.html'  # You can customize the template path if needed

admin.site.login = CustomLoginView.as_view()


class UserBioAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'department',
        'tel',
        'code',
        'qrcode'
    ]

admin.site.register(User, UserAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(UserBio, UserBioAdmin)
# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)
