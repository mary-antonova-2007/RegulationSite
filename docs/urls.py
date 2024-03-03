from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.project_list, name='project_list'),
    path('projects/<int:project_id>/', views.project_details, name='project_details'),
    path('product/<int:product_id>/', views.view_product, name='product_details'),
    path('documents/download/<int:document_id>/', views.download_document, name='download_document'),
    path('archive_document/<int:document_id>/', views.archive_document, name='archive_document'),
    path('archive_document_from_product/<int:document_id>/', views.archive_document_from_product, name='archive_document_from_product'),
    path('documents/open_document/<int:document_id>/', views.open_document, name='open_document'),
]
