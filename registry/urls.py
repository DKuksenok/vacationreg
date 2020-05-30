from django.urls import path

from . import views

app_name = 'registry'
urlpatterns = [
    path('', views.EmployeesView.as_view()),
    path('download/vacation', views.export_vacations, name='download-vacation'),
    path('employees/', views.EmployeesView.as_view(), name='employees'),
    path('employees/dismissal', views.EmployeesDismissalView.as_view(), name='employees-dismissal'),
    path('employees/in-vacation', views.EmployeesVacationView.as_view(), name='employees-vacation'),
    path('employees/at-work', views.EmployeesAtWorkView.as_view(), name='employees-at-work'),
    path('employees/serch', views.SearchResultView.as_view(), name='search'),
    path('<slug:slug>/', views.EmployeeDetailView.as_view(), name='employee-detail'),
    path('<slug:slug>/vacation/add', views.EmployeeDetailView.as_view(), name='vacation-add-by-user'),
    path('<slug:slug>/vacation/edit/<int:pk>', views.EmployeeDetailView.as_view(), name='vacation-edit-by-user'),
    path('<slug:slug>/vacation/delete/<int:pk>', views.EmployeeDetailView.as_view(), name='vacation-edit-by-user'),
]