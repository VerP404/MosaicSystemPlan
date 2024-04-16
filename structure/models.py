from django.db import models

from reference.models import StructuralSubdivision, Profile, Specialty, BranchCode


class PlanType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название", unique=True)
    description = models.CharField(max_length=200, verbose_name="Описание", default='-')
    list_targets = models.CharField(max_length=200, verbose_name="Цели ОМС", default='-')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип плана'
        verbose_name_plural = 'Типы планов'


class PlanSubtype(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    plan_type = models.ForeignKey(PlanType, on_delete=models.CASCADE)
    description = models.CharField(max_length=200, verbose_name="Описание", default='-')
    list_targets = models.CharField(max_length=200, verbose_name="Цели ОМС", default='-')

    def __str__(self):
        return f"{self.plan_type.name} - {self.name}"  # Возвращаем строку "Тип плана - Подтип плана"

    class Meta:
        verbose_name = 'Подтип плана'
        verbose_name_plural = 'Подтипы плана'
        unique_together = (('name', 'plan_type'),)


class MedicalOrganization(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название", unique=True)
    short_name = models.CharField(max_length=255, verbose_name="Краткое название", default='-')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'


class Corpus(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    organization = models.ForeignKey(MedicalOrganization, on_delete=models.CASCADE)
    short_name = models.CharField(max_length=255, verbose_name="Краткое название", default='-')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Корпус'
        verbose_name_plural = 'Корпуса'
        unique_together = (('name', 'organization'),)


class Department(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    building = models.ForeignKey(Corpus, on_delete=models.CASCADE)
    short_name = models.CharField(max_length=255, verbose_name="Краткое название", default='-')
    plan_subtypes = models.ManyToManyField(PlanSubtype, verbose_name='Подтип плана', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Отделение'
        verbose_name_plural = 'Отделения'
        unique_together = (('name', 'building'),)


class Doctor(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='Отделение')
    snils = models.CharField(max_length=20, verbose_name='СНИЛС')
    surname = models.CharField(max_length=100, verbose_name='Фамилия')
    name = models.CharField(max_length=100, verbose_name='Имя')
    patronymic_name = models.CharField(max_length=100, verbose_name='Отчество')
    birth_date = models.DateField(verbose_name='Дата рождения')
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='Пол')
    start_date = models.DateField(verbose_name='Дата приема')
    end_date = models.DateField(null=True, blank=True, verbose_name='Дата увольнения')

    # Добавляем справочники
    structural_subdivision = models.ForeignKey(
        StructuralSubdivision,
        on_delete=models.PROTECT,
        verbose_name='Подразделение',
        default=None)
    profile = models.ForeignKey(
        Profile,
        on_delete=models.PROTECT,
        verbose_name='Профиль',
        default=None)
    specialty = models.ForeignKey(
        Specialty,
        on_delete=models.PROTECT,
        verbose_name='Специальность',
        default=None)
    branch_code = models.ForeignKey(
        BranchCode,
        on_delete=models.PROTECT,
        verbose_name='Код отделения',
        default=None)

    certificate_validity_date = models.DateField(null=True, blank=True, verbose_name='Сертификат действителен по:')

    def __str__(self):
        return self.name

    @property
    def deleted_message(self):
        return "Удалено"

    class Meta:
        verbose_name = 'Врач'
        verbose_name_plural = 'Врачи'
        unique_together = (('department', 'surname', 'name', 'patronymic_name', 'structural_subdivision', 'specialty'),)
