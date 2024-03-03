from django.urls import path
from . import views

urlpatterns = [
    # другие URL-пути
    path('notifications/', views.notifications_view, name='notifications'),
    path('mark-notifications-read/', views.mark_notifications_as_read, name='mark_notifications_read'),
]