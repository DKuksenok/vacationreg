from django.db import models
from django.utils import timezone
from django.db.models import Q
from .services import get_qs_for_vacation

class Employee(models.Model):
    username = models.SlugField(
        'логин',
        unique=True
    )
    first_name = models.CharField(
        'имя',
        max_length=50
    )
    middle_name = models.CharField(
        'отчество',
        max_length=50,
        null=True,
        blank=True
    )
    last_name = models.CharField(
        'фамилия',
        max_length=50
    )
    dismissal_date = models.DateField(
        'дата увольнения',
        null=True,
        blank=True
    )
    dismissal_order = models.CharField(
        'приказ об увольнении',
        max_length=50,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "сотрудник"
        verbose_name_plural = "сотрудники"
        ordering = ['last_name', 'first_name', 'middle_name']

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return "%s %s %s" % (self.last_name, self.first_name, self.middle_name)

    @property
    def is_dismissal(self):
        if self.dismissal_date is None:
            return False
        else:
            return self.dismissal_date <= timezone.now().date()

    def in_vacation(date=timezone.now().date()):
        qs = get_qs_for_vacation(date)
        return Employee.objects.filter(
            ~qs.on_dismissal & ~qs.on_review & qs.on_vacation
        ).distinct()

    def not_in_vacation(date=timezone.now().date()):
        qs = get_qs_for_vacation(date)
        return Employee.objects.filter(
            (~qs.on_dismissal & ~qs.on_vacation) | qs.on_review
        ).distinct()

    def get_qs_usernames_in_vacation(date=timezone.now()):
        qs = get_qs_for_vacation(date)
        return Employee.objects.filter(
            ~qs.on_dismissal & ~qs.on_review & qs.on_vacation
        ).distinct().order_by('username').values_list('username')

class Vacation(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField('начало отпуска')
    end_date = models.DateField('конец отпуска')
    description = models.CharField('основание', max_length=100)

    class Meta:
        verbose_name = "отпуск"
        verbose_name_plural = "отпуска"

class VacationReview(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField('начало отзыва из отпуска')
    end_date = models.DateField('конец отзыва из отпуска')
    description = models.CharField('основание', max_length=100)

    class Meta:
        verbose_name = "отзыв"
        verbose_name_plural = "отзывы"
