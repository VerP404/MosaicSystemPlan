from django.contrib import admin
from plan.models import PlanDepartment, Plan, PlanRecordDoctor, PlanDoctor


class PlanInline(admin.TabularInline):
    model = Plan
    extra = 0  # Указываем 0, чтобы не позволять добавлять новые записи
    can_delete = False  # Запрещаем удалять существующие записи
    readonly_fields = ['month']
    fields = ['month', 'plan_integer', 'plan_money']
    ordering = ['month']

    def has_add_permission(self, request, obj):
        return False  # Запрещаем добавление новых записей

    def has_change_permission(self, request, obj=None):
        return True  # Разрешаем редактирование существующих записей

    def has_delete_permission(self, request, obj=None):
        return False  # Запрещаем удаление существующих записей


class PlanDepartmentAdmin(admin.ModelAdmin):
    inlines = [PlanInline]
    list_display = ['plan_subtype', 'department', 'corpus', 'total_integer', 'total_money']

    def total_integer(self, obj):
        # Вычисляем общее количество талонов (plan_integer) для данного PlanDepartment
        return sum(obj.plan_set.values_list('plan_integer', flat=True))

    def total_money(self, obj):
        # Вычисляем общую сумму денег (plan_money) для данного PlanDepartment
        return sum(obj.plan_set.values_list('plan_money', flat=True))

    # Переименуем колонки
    total_integer.short_description = 'Всего талонов'
    total_money.short_description = 'Всего финансы'


class PlanAdmin(admin.ModelAdmin):
    list_display = ['plan_department', 'month', 'plan_integer', 'plan_money']
    ordering = ['plan_department', 'month']


class PlanRecordDoctorInline(admin.TabularInline):
    model = PlanRecordDoctor
    extra = 0  # Указываем 0, чтобы не позволять добавлять новые записи
    can_delete = False  # Запрещаем удалять существующие записи
    readonly_fields = ['month']
    fields = ['month', 'plan_integer', 'plan_money']
    ordering = ['month']

    def has_add_permission(self, request, obj):
        return False  # Запрещаем добавление новых записей

    def has_change_permission(self, request, obj=None):
        return True  # Разрешаем редактирование существующих записей

    def has_delete_permission(self, request, obj=None):
        return False  # Запрещаем удаление существующих записей


class PlanDoctorAdmin(admin.ModelAdmin):
    inlines = [PlanRecordDoctorInline]
    list_display = ['doctor', 'plan_subtype', 'department', 'corpus', 'total_integer', 'total_money']

    def total_integer(self, obj):
        # Вычисляем общее количество талонов (plan_integer) для данного PlanDoctor
        return sum(obj.planrecorddoctor_set.values_list('plan_integer', flat=True))

    def total_money(self, obj):
        # Вычисляем общую сумму денег (plan_money) для данного PlanDoctor
        return sum(obj.planrecorddoctor_set.values_list('plan_money', flat=True))

    # Переименуем колонки
    total_integer.short_description = 'Всего талонов'
    total_money.short_description = 'Всего финансы'


class PlanRecordDoctorAdmin(admin.ModelAdmin):
    list_display = ['plan_doctor', 'month', 'plan_integer', 'plan_money']
    ordering = ['plan_doctor', 'month']


admin.site.register(PlanDepartment, PlanDepartmentAdmin)
admin.site.register(Plan, PlanAdmin)

admin.site.register(PlanDoctor, PlanDoctorAdmin)
admin.site.register(PlanRecordDoctor, PlanRecordDoctorAdmin)


admin.site.site_header = 'МозаикаМед - Система ведения планов'
