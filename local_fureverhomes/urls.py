from django.contrib import admin
from fureverhomes_users_app import views
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path('', views.home, name='home'),
    path('login_error/', views.error, name='error'),
    path('create_account/', views.create_account_page, name='create_account'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
