import csv
from django.contrib import admin
from django.http import HttpResponse
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import Profile

class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"

class ProfileResource(resources.ModelResource):
    class Meta:
        model = Profile
        exclude = ('password', 'user_permissions', 'groups', 'last_login', 'date_joined', 'is_active')

class ProfileAdmin(ImportExportModelAdmin, admin.ModelAdmin, ExportCsvMixin):
    resource_class = ProfileResource
    actions = ["export_as_csv"]
    exclude = ('password', 'user_permissions', 'groups', 'last_login', 'date_joined', 'is_active')
    list_display = ('username', 'first_name', 'last_name', 'course', 'year', 'team', 'post', 'is_member')
    search_fields = ('first_name', 'last_name', 'email', 'mobile_number')
    list_filter = ('course', 'year', 'team', 'post', 'gender', 'is_member')
    list_export = ('id', 'first_name', 'last_name', 'email', 'course', 'year', 'team', 'post', 'gender', 'mobile_number', 'is_member')

admin.site.register(Profile, ProfileAdmin)
