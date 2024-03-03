from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('change_password/', views.change_password, name='change_password'),
    path('edit-profile/', views.edit_profile_view, name='edit_profile'),
]
