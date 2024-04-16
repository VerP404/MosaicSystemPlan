from django.db import models
from structure.models import Department, PlanSubtype, Corpus, MedicalOrganization, Doctor

MONTH_CHOICES = [
    ('01', 'Январь'),
    ('02', 'Февраль'),
    ('03', 'Март'),
    ('04', 'Апрель'),
    ('05', 'Май'),
    ('06', 'Июнь'),
    ('07', 'Июль'),
    ('08', 'Август'),
    ('09', 'Сентябрь'),
    ('10', 'Октябрь'),
    ('11', 'Ноябрь'),
    ('12', 'Декабрь'),
]


class PlanDepartment(models.Model):
    corpus = models.ForeignKey(Corpus, on_delete=models.CASCADE, verbose_name='Корпус')
    organization = models.ForeignKey(MedicalOrganization, on_delete=models.CASCADE, verbose_name='Организация')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='Отделение')
    plan_subtype = models.ForeignKey(PlanSubtype, on_delete=models.CASCADE, verbose_name='Подтип плана')

    def __str__(self):
        return f'{self.department} - {self.plan_subtype}'

    class Meta:
        verbose_name = 'План отделения'
        verbose_name_plural = 'Планы отделений'


class Plan(models.Model):
    month = models.CharField(max_length=2, choices=MONTH_CHOICES, verbose_name='Месяц')
    plan_integer = models.IntegerField(default=0, verbose_name='Талоны')
    plan_money = models.DecimalField(default=0, max_digits=10, decimal_places=2,
                                     verbose_name='Финансы')
    plan_department = models.ForeignKey(PlanDepartment, on_delete=models.CASCADE, verbose_name='План отделения')

    def __str__(self):
        return self.month

    class Meta:
        verbose_name = 'Месячный план отделения'
        verbose_name_plural = 'Месячные планы отделений'


class PlanDoctor(models.Model):
    corpus = models.ForeignKey(Corpus, on_delete=models.CASCADE, verbose_name='Корпус')
    organization = models.ForeignKey(MedicalOrganization, on_delete=models.CASCADE, verbose_name='Организация')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='Отделение')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='plans', verbose_name='Врач')
    plan_subtype = models.ForeignKey(PlanSubtype, on_delete=models.CASCADE, verbose_name='Подтип плана')

    def __str__(self):
        return f'{self.doctor} - {self.department} - {self.plan_subtype}'

    class Meta:
        verbose_name = 'План врача'
        verbose_name_plural = 'Планы врачей'


class PlanRecordDoctor(models.Model):
    month = models.CharField(max_length=2, choices=MONTH_CHOICES, verbose_name='Месяц')
    plan_integer = models.IntegerField(default=0, verbose_name='Талоны')
    plan_money = models.DecimalField(default=0, max_digits=10, decimal_places=2,
                                     verbose_name='Финансы')
    plan_doctor = models.ForeignKey(PlanDoctor, on_delete=models.CASCADE, verbose_name='План отделения')

    def __str__(self):
        return self.month

    class Meta:
        verbose_name = 'Месячный план врача'
        verbose_name_plural = 'Месячные планы врачей'
