from django.urls import path
from . import views

urlpatterns = [
    path('add_task/', views.add_task, name='add_task'),
    path('add_task/load_products/', views.load_products, name='ajax_load_products'),
    path('add_task/load_predecessors/', views.load_predecessors, name='ajax_load_predecessors'),
    path('gantt-chart/', views.gantt_chart_view, name='gantt_chart'),
]
