from django.contrib import admin
from fureverhomes_users_app import views
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path('', views.home, name='home'),
    path('login_error/', views.error, name='error'),
    path('select_account_type/', views.select_account_type, name='select_account_type'),
    path('create_co_account/', views.create_co_account, name='create_co_account'),
    path('create_fo_account/', views.create_fo_account, name='create_fo_account'),
    path('co_dashboard/', views.co_dashboard, name='co_dashboard'),
    path('fo_dashboard/', views.fo_dashboard, name='fo_dashboard'),
]
