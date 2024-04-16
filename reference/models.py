from django.db import models


class StructuralSubdivision(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование подразделения')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Подразделения'


class Profile(models.Model):
    name = models.CharField(max_length=255, verbose_name='Профиль')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Профили'


class Specialty(models.Model):
    name = models.CharField(max_length=255, verbose_name='Специальность')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Специальности'


class BranchCode(models.Model):
    name = models.CharField(max_length=50, verbose_name='Код отделения')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Отделения'
