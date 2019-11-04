from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe
from django.contrib.auth.models import Group
admin.site.unregister(Group)


class UserAdmin(admin.ModelAdmin):
    list_display_links = None
    list_display = ['email', 'is_superuser', 'Action']

    exclude = (
        'password', 'groups', 'user_permissions',
        'first_name', 'last_name', 'last_login', 'date_joined'
    )

    def Action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; ' href='/admin/search_module/myuser/{}/change/'>View/Edit</a>".format(obj.id))

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(MyUser, UserAdmin)


class StudentAddressInline(admin.TabularInline):
    model = Address
    max_num = 1


class StudentAdmin(admin.ModelAdmin):
    list_display_links = None
    inlines = [StudentAddressInline, ]
    list_display = ['username', 'Action']

    def Action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; ' href='/admin/search_module/student/{}/change/'>View/Edit</a>".format(obj.id))


admin.site.register(Student, StudentAdmin)