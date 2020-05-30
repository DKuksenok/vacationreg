from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.views import generic
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .services import qs_to_csv_response

from .models import Employee, Vacation, VacationReview

class EmployeeDetailView(LoginRequiredMixin, generic.DetailView):
    model = Employee
    context_object_name = 'employee'
    slug_field = 'username'

class EmployeesView(LoginRequiredMixin, generic.ListView):
    paginate_by = 50 # количество объектов на странице
    model = Employee
    template_name = 'registry/employee_list.html'

class EmployeesDismissalView(LoginRequiredMixin, generic.ListView):
    paginate_by = 50 # количество объектов на странице
    model = Employee
    template_name = 'registry/employee_list.html'

    def get_queryset(self):
        return Employee.objects.filter(Q(dismissal_date__isnull=False) & Q(dismissal_date__lte=timezone.now()))

class EmployeesAtWorkView(LoginRequiredMixin, generic.ListView):
    paginate_by = 50 # количество объектов на странице
    model = Employee
    template_name = 'registry/employee_list.html'

    def get_queryset(self):
        date = timezone.now().date()
        return Employee.not_in_vacation(date)

class EmployeesVacationView(LoginRequiredMixin, generic.ListView):
    paginate_by = 50 # количество объектов на странице
    model = Employee
    template_name = 'registry/employee_list.html'

    def get_queryset(self):
        date = timezone.now().date()
        return Employee.in_vacation(date)

class SearchResultView(LoginRequiredMixin, generic.ListView):
    paginate_by = 50
    model = Employee
    template_name = 'registry/employee_list.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Employee.objects.filter(
            Q(first_name__icontains=query) |
            Q(middle_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(username__icontains=query)
        )

def export_vacations(request):
    date = timezone.now().date()
    return qs_to_csv_response(Employee.get_qs_usernames_in_vacation(date), 'vacations')