from django.db.models.signals import m2m_changed, post_save, pre_save
from django.dispatch import receiver
from structure.models import Department, Doctor
from structure.models import PlanSubtype
from plan.models import PlanDepartment, Plan, PlanRecordDoctor, PlanDoctor, MONTH_CHOICES


@receiver(m2m_changed, sender=Department.plan_subtypes.through)
def create_plan_department_instances(sender, instance, action, model, pk_set, **kwargs):
    if action == 'post_add':
        for pk in pk_set:
            plan_subtype = PlanSubtype.objects.get(pk=pk)
            PlanDepartment.objects.get_or_create(
                corpus=instance.building,
                organization=instance.building.organization,
                department=instance,
                plan_subtype=plan_subtype
            )


@receiver(post_save, sender=PlanDepartment)
def create_missing_plans(sender, instance, created, **kwargs):
    if created:
        existing_plans = Plan.objects.filter(plan_department=instance)
        for month_choice in MONTH_CHOICES:
            month = month_choice[0]
            # Проверяем, не создан ли уже план на этот месяц
            if not existing_plans.filter(month=month).exists():
                Plan.objects.create(
                    month=month,
                    plan_department=instance
                )


# Сигнал для создания записей PlanDoctor и PlanRecordDoctor при создании нового объекта PlanDepartment
@receiver(post_save, sender=PlanDepartment)
def create_plan_doctors_and_records(sender, instance, created, **kwargs):
    if created:
        department = instance.department
        plan_subtype_list = department.plan_subtypes.all()
        doctors = department.doctor_set.all()

        for plan_subtype in plan_subtype_list:
            for doctor in doctors:
                # Создаем запись PlanDoctor
                plan_doctor, _ = PlanDoctor.objects.get_or_create(
                    corpus=instance.corpus,
                    organization=instance.organization,
                    department=department,
                    doctor=doctor,
                    plan_subtype=plan_subtype
                )

                # Создаем записи PlanRecordDoctor для каждого месяца из MONTH_CHOICES
                for month, month_name in MONTH_CHOICES:
                    PlanRecordDoctor.objects.create(
                        month=month,
                        plan_integer=0,
                        plan_money=0.0,
                        plan_doctor=plan_doctor
                    )


# Сигнал для создания записей PlanDoctor при сохранении нового объекта Doctor
@receiver(post_save, sender=Doctor)
def create_plan_doctors_for_doctor(sender, instance, created, **kwargs):
    if created:
        department = instance.department
        if department:
            plan_subtype_list = department.plan_subtypes.all()
            print(department.building.organization)
            for plan_subtype in plan_subtype_list:
                # Создаем запись PlanDoctor для каждого подтипа плана
                plan_doctor, _ = PlanDoctor.objects.get_or_create(
                    corpus=department.building,
                    organization=department.building.organization,
                    department=department,
                    doctor=instance,
                    plan_subtype=plan_subtype
                )

                # Создаем записи PlanRecordDoctor для каждого месяца из MONTH_CHOICES
                for month, month_name in MONTH_CHOICES:
                    PlanRecordDoctor.objects.create(
                        month=month,
                        plan_integer=0,
                        plan_money=0.0,
                        plan_doctor=plan_doctor  # Связываем запись с созданным PlanDoctor
                    )


# Сигнал для удаления записей Plan, PlanDepartment, PlanDoctor и PlanRecordDoctor
# при удалении подтипов плана из отделения
@receiver(m2m_changed, sender=Department.plan_subtypes.through)
def delete_plan_doctors_and_records(sender, instance, action, model, pk_set, **kwargs):
    if action == 'post_remove':

        # Находим все записи PlanDepartment для данного отделения и удаленных подтипов плана
        plan_departments = PlanDepartment.objects.filter(department=instance, plan_subtype__in=pk_set)

        # Для каждой записи PlanDepartment удаляем связанные записи PlanDoctor и PlanRecordDoctor
        for plan_department in plan_departments:
            plan_doctors = PlanDoctor.objects.filter(department=plan_department.department,
                                                     plan_subtype=plan_department.plan_subtype,
                                                     doctor__department=plan_department.department)
            plan_doctors.delete()

            plan_record_doctors = PlanRecordDoctor.objects.filter(plan_doctor__in=plan_doctors)
            plan_record_doctors.delete()

        # Найти все связанные записи PlanDepartment и удалить их
        PlanDepartment.objects.filter(department=instance, plan_subtype__in=pk_set).delete()

        # Найти все связанные записи Plan и удалить их
        Plan.objects.filter(plan_department__department=instance, plan_department__plan_subtype__in=pk_set).delete()


# Сигнал для обновления планов при изменении отделения у врача
@receiver(pre_save, sender=Doctor)
def update_plans_on_department_change(sender, instance, **kwargs):
    if instance.pk:  # Если объект уже существует (изменение)
        try:
            original_instance = Doctor.objects.get(pk=instance.pk)
        except Doctor.DoesNotExist:
            return

        # Проверяем, изменилось ли отделение
        if original_instance.department != instance.department:
            # Удаляем старые записи PlanDoctor и PlanRecordDoctor
            PlanDoctor.objects.filter(doctor=instance).delete()
            PlanRecordDoctor.objects.filter(plan_doctor__doctor=instance).delete()

            # Создаем новые записи PlanDoctor и PlanRecordDoctor для нового отделения
            if instance.department:
                department = instance.department
                plan_subtype_list = department.plan_subtypes.all()

                for plan_subtype in plan_subtype_list:
                    # Создаем запись PlanDoctor для каждого подтипа плана
                    plan_doctor, _ = PlanDoctor.objects.get_or_create(
                        corpus=department.building,
                        organization=department.building.organization,
                        department=department,
                        doctor=instance,
                        plan_subtype=plan_subtype
                    )

                    # Создаем записи PlanRecordDoctor для каждого месяца из MONTH_CHOICES
                    for month, month_name in MONTH_CHOICES:
                        PlanRecordDoctor.objects.create(
                            month=month,
                            plan_integer=0,
                            plan_money=0.0,
                            plan_doctor=plan_doctor  # Связываем запись с созданным PlanDoctor
                        )
