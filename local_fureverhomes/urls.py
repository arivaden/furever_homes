from django.contrib import admin
from fureverhomes_users_app import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path('', views.home, name='home'),
    path('login_error/', views.error, name='error'),
    path('select_account_type/', views.select_account_type, name='select_account_type'),
    path('create_co_account/', views.create_co_account, name='create_co_account'),
    path('create_fo_account/', views.create_fo_account, name='create_fo_account'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('co_dashboard/', views.co_dashboard, name='co_dashboard'),
    path('fo_dashboard/', views.fo_dashboard, name='fo_dashboard'),
    path('select_pet_type/', views.select_pet_type, name='select_pet_type'),
    path('create_dog_profile/', views.create_dog_profile, name="create_dog_profile"),
    path('create_cat_profile/', views.create_cat_profile, name="create_cat_profile"),
    path('pet_profile/<int:pet_profile_id>', views.pet_profile, name='pet_profile'),
    path('code_of_conduct', views.code_of_conduct, name='code_of_conduct'),
    path('delete_pet_profile/<int:pet_profile_id>', views.delete_pet_profile, name='delete_pet_profile'),
    path('delete_pet_profile/<int:pet_profile_id>', views.delete_pet_profile, name='delete_pet_profile'),
    path('mark_as_interested/<int:pet_profile_id>/<int:user_id>', views.mark_as_interested, name='mark_as_interested')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
