from django.contrib.auth import views
from django.urls import path

app_name = 'accounts'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('logout-then-login', views.logout_then_login, name='logout-then-login')
]