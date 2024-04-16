from django.contrib import admin
from django.contrib.admin import AdminSite

from structure.models import PlanSubtype, PlanType, Corpus, MedicalOrganization, Department, Doctor


class PlanSubtypeInline(admin.TabularInline):
    model = PlanSubtype
    extra = 0  # Устанавливаем extra в 0, чтобы не создавать автоматически пустые строки


class PlanTypeAdmin(admin.ModelAdmin):
    inlines = [PlanSubtypeInline]
    list_display = ('name', 'description', 'list_targets')


class CorpusInline(admin.TabularInline):
    model = Corpus
    extra = 0  # Устанавливаем extra в 0, чтобы не создавать автоматически пустые строки


class MedicalOrganizationAdmin(admin.ModelAdmin):
    inlines = [CorpusInline]
    list_display = ('name', 'short_name')


class DepartmentAdmin(admin.ModelAdmin):
    model = Department
    filter_horizontal = ('plan_subtypes',)
    list_display = ('name', 'building', 'short_name')


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'patronymic_name', 'department', 'start_date', 'end_date', 'specialty')

class MyAdminSite(AdminSite):
    site_header = 'Справочники'


my_admin_site = MyAdminSite(name='myadmin')

admin.site.register(PlanType, PlanTypeAdmin)
admin.site.register(MedicalOrganization, MedicalOrganizationAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Doctor, DoctorAdmin)


