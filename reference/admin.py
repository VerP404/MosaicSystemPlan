from django.contrib import admin
from reference.models import StructuralSubdivision, Profile, Specialty, BranchCode
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources


class StructuralSubdivisionResource(resources.ModelResource):
    class Meta:
        model = StructuralSubdivision


class StructuralSubdivisionAdmin(ImportExportActionModelAdmin):
    resources = StructuralSubdivisionResource


class ProfileResource(resources.ModelResource):
    class Meta:
        model = Profile


class ProfileAdmin(ImportExportActionModelAdmin):
    resources = ProfileResource


class SpecialtyResource(resources.ModelResource):
    class Meta:
        model = Specialty


class SpecialtyAdmin(ImportExportActionModelAdmin):
    resources = SpecialtyResource


class BranchCodeResource(resources.ModelResource):
    class Meta:
        model = BranchCode


class BranchCodeAdmin(ImportExportActionModelAdmin):
    resources = BranchCodeResource


admin.site.register(StructuralSubdivision, StructuralSubdivisionAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Specialty, SpecialtyAdmin)
admin.site.register(BranchCode, BranchCodeAdmin)
