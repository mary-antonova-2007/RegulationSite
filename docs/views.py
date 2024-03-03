from notification.models import Notification
from django.contrib.auth.models import Group
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect, FileResponse
from .models import Product, WorkDocument, Project
from .forms import WorkDocumentForm
from collections import defaultdict
from django.contrib.auth.decorators import login_required


import os
from urllib.parse import quote


# Create your views here.
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'docs/project_list.html', {'projects': projects})


@login_required
def project_details(request, project_id):
    can_edit_docs = False
    current_user = request.user
    project = get_object_or_404(Project, id=project_id)
    if project.project_manager:
        if current_user.id == project.project_manager.id:
            can_edit_docs = True
    if project.project_designer:
        if current_user.id == project.project_designer.id:
            can_edit_docs = True
    products = Product.objects.filter(project=project)
    project_documents = WorkDocument.objects.filter(project=project, isArchived=False, product__isnull=True)
    archived_documents = WorkDocument.objects.filter(project=project, isArchived=True, product__isnull=True)
    documents_grouped = defaultdict(list)
    # Группировка документов
    for document in project_documents:
        documents_grouped[document.document_type.name].append(document)
    # Группировка изделий по комнатам
    products_grouped_by_room = defaultdict(list)
    for product in products:
        room = product.room if product.room else 'Без комнаты'
        products_grouped_by_room[room].append(product)

    if request.method == 'POST':
        form = WorkDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            new_document = form.save(commit=False)
            new_document.project = project

            if new_document.document_type.isSingleton:
                # Архивация старых документов того же типа
                WorkDocument.objects.filter(
                    project=project,
                    document_type=new_document.document_type,
                    isArchived=False,
                    product__isnull=True,
                ).update(isArchived=True)

            # Определение типа изменения
            if new_document.document_type.isSingleton:
                existing_docs = WorkDocument.objects.filter(
                    product=product,
                    document_type=new_document.document_type,
                    product__isnull=True,
                    isArchived=False
                )
                was_existing = existing_docs.exists()
                existing_docs.update(isArchived=True)
                if was_existing:
                    message = "Обновлен документ"
                    message_type = 'document_change'
                else:
                    message = "Добавлен документ"
                    message_type = 'document_add_to_project'
            else:
                message = "Добавлен документ"
                message_type = 'document_add_to_project'
            new_document.save()
            new_document.start_backup()
            # Создание уведомлений
            create_notifications(
                from_user=request.user,
                product=product,
                project=product.project,
                document=new_document,
                message=message,
                message_type=message_type,
            )
            return HttpResponseRedirect(request.path_info)
    else:
        form = WorkDocumentForm()

    context = {
        'project': project,
        'products': products,
        'project_documents_grouped': dict(documents_grouped),
        'archived_documents': archived_documents,
        'form': form,
        'products_grouped_by_room': dict(products_grouped_by_room),
        'can_edit_docs': can_edit_docs
    }

    return render(request, 'docs/project_details.html', context)


def download_document(request, document_id):
    try:
        # Получаем документ по ID
        document = WorkDocument.objects.get(id=document_id)

        # Путь к файлу
        file_path = document.content.path

        # Открыть файл для чтения в бинарном режиме
        with open(file_path, 'rb') as fh:
            # Создаем HTTP ответ с содержимым файла
            response = HttpResponse(fh.read(), content_type="application/octet-stream")
            # Установка заголовка, который предлагает имя файла
            file_name = os.path.basename(file_path)
            safe_file_name = quote(file_name)
            response['Content-Disposition'] = f'attachment; filename="{safe_file_name}"'
            print("File name:", os.path.basename(file_path))
            return response
    except WorkDocument.DoesNotExist:
        # Если документ не найден, возвращаем ошибку 404
        raise Http404("Документ не найден")
    except IOError:
        # Ошибка при открытии файла
        raise Http404("Ошибка при чтении файла")


@login_required
def view_product(request, product_id):
    can_edit_docs = False
    current_user = request.user
    product = get_object_or_404(Product, id=product_id)
    if product.product_designer.id == current_user.id:
        can_edit_docs = True
    if product.project.project_designer == current_user.id:
        can_edit_docs = True

    documents = WorkDocument.objects.filter(product=product, isArchived=False)
    archived_documents = WorkDocument.objects.filter(product=product, isArchived=True)
    # Делаем backup для документов если они не сохранялись
    backup_docs_if_not(documents)
    # Группировка документов по типу
    documents_grouped = defaultdict(list)
    for document in documents:
        documents_grouped[document.document_type.name].append(document)

    if request.method == 'POST':
        form = WorkDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            new_document = form.save(commit=False)
            new_document.product = product

            # Определение типа изменения
            if new_document.document_type.isSingleton:
                existing_docs = WorkDocument.objects.filter(
                    product=product,
                    document_type=new_document.document_type,
                    isArchived=False,
                    product__isnull=False,
                )
                was_existing = existing_docs.exists()
                existing_docs.update(isArchived=True)

                if was_existing:
                    message = "Обновлен документ"
                    message_type = 'document_change'
                else:
                    message = "Добавлен документ"
                    message_type = 'document_add_to_product'
            else:
                message = "Добавлен документ"
                message_type = 'document_add_to_product'

            new_document.save()
            new_document.start_backup()
            # Создание уведомлений
            create_notifications(
                from_user=request.user,
                product=product,
                project=product.project,
                document=new_document,
                message=message,
                message_type=message_type
            )

            return redirect('product_details', product_id=product_id)
    else:
        form = WorkDocumentForm()

    context = {
        'product': product,
        'documents_grouped': dict(documents_grouped),
        'archived_documents': archived_documents,
        'form': form,
        'can_edit_docs': can_edit_docs,
    }

    return render(request, 'docs/product_detail.html', context)


def create_notifications(from_user, product: Product, project: Project, document, message, message_type):
    recipients = []
    if project:
        if project.project_manager:
            recipients.append(project.project_manager)
        if project.project_designer:
            recipients.append(project.project_designer)
    if document.document_type.name == "ВПИ Excel":
        supply_heads_group = Group.objects.get(name="Снабжение")
        recipients.extend(supply_heads_group.user_set.all())
    # Если изделие
    if product:
        # Определение получателя уведомления
        if not document.document_type.name == "Чертежи КДЗ":
            production_heads_group = Group.objects.get(name="Производство")
            # Добавление пользователей из группы "Производство" в список recipients
            recipients.extend(production_heads_group.user_set.all())

    # Удаление повторяющихся получателей
    unique_recipients = list(set(recipients))

    # Создание уведомления для каждого уникального получателя
    for recipient in unique_recipients:
        Notification.objects.create(
            from_user=from_user,
            recipient=recipient,
            message=message,
            type=message_type,
            product=product,
            project=project,
            work_document=document,
        )


def archive_document(request, document_id):
    document = get_object_or_404(WorkDocument, id=document_id)
    document.isArchived = True
    document.save()
    return HttpResponseRedirect(reverse('project_details', args=[document.project.id]))


def archive_document_from_product(request, document_id):
    document = get_object_or_404(WorkDocument, id=document_id)
    document.isArchived = True
    document.save()
    return HttpResponseRedirect(reverse('product_details', args=[document.product.id]))


def open_document(request, document_id):
    document = get_object_or_404(WorkDocument, id=document_id)
    # Здесь предполагается, что у вас есть поле `file` в модели Document,
    # которое хранит путь к файлу документа
    document_path = document.content.path
    response = FileResponse(open(document_path, 'rb'))
    return response


def backup_docs_if_not(docs):
    for doc in docs:
        if not doc.backup_saved:
            doc.start_backup()

