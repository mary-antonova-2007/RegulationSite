# Create your views here.
from functions.text import process_content
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SectionForm, ImageForm, FileForm
from .models import Section, Image, File
from docs.models import Product, Project
from django.forms import inlineformset_factory
from django.http import JsonResponse
from notification.models import Notification
from django.db import models


def index(request):
    root_section = Section.objects.get(name='Root')
    return section_page(request, root_section.id)


def section_page(request, section_id):
    section = Section.objects.get(id=section_id)
    processed_content = process_content(section.content)
    images = Image.objects.filter(section=section)
    files = File.objects.filter(section=section)
    sub_sections = Section.objects.filter(parent=section)
    return render(request, 'section_template.html', {
        'section': section,
        'images': images,
        'files': files,
        'sub_sections': sub_sections,
        'processed_content': processed_content,
    })


def edit_section(request, section_id):
    section = Section.objects.get(pk=section_id)
    ImageFormset = inlineformset_factory(Section, Image, form=ImageForm, extra=1, can_delete=True)
    FileFormset = inlineformset_factory(Section, File, form=FileForm, extra=1, can_delete=True)

    if request.method == 'POST':
        form = SectionForm(request.POST, instance=section)
        image_formset = ImageFormset(request.POST, request.FILES, instance=section)
        file_formset = FileFormset(request.POST, request.FILES, instance=section)

        # Обработка удаления изображений
        for image_form in image_formset.deleted_forms:
            if image_form.instance.pk:
                image_form.instance.delete()

        # Проверка валидности
        if form.is_valid() and file_formset.is_valid():
            valid_image_forms = all(
                image_form.is_valid() or not image_form.has_changed() for image_form in image_formset)
            print(valid_image_forms)
            if valid_image_forms:
                print('before form save')
                form.save()
                print('after form save')
                print('before image_formset save')
                image_formset.save()
                print('after image_formset save')
                print('before file_formset save')
                file_formset.save()
                print('after file_formset save')
                return redirect('section_page', section_id=section.id)
            else:
                return redirect('edit_section', section_id=section.id)
        else:
            print("Form errors:", form.errors)
            for idx, image_form in enumerate(image_formset):
                print(f"Image form {idx} errors:", image_form.errors)
            for idx, file_form in enumerate(file_formset):
                print(f"File form {idx} errors:", file_form.errors)

    else:
        form = SectionForm(instance=section)
        image_formset = ImageFormset(instance=section)
        file_formset = FileFormset(instance=section)

    return render(request, 'section_form.html', {
        'section_form': form,
        'image_formset': image_formset,
        'file_formset': file_formset
    })


def search_results(request):
    query = request.GET.get('query', '')
    products = []
    projects = []
    products_sorted_by_product = dict()
    if query:
        sections = Section.objects.filter(content__icontains=query)
        all_products = Product.objects.all()
        all_projects = Project.objects.all()
        products = list(set(search(query, all_products, ['name', 'designation'])))
        projects = list(set(search(query, all_projects, ['name', 'designation'])))
        for prod in products:
            proj = prod.project
            if proj in products_sorted_by_product:
                products_sorted_by_product[proj].append(prod)
            else:
                products_sorted_by_product[proj] = [prod]
        # Применение process_content к каждому разделу
        for section in sections:
            section.processed_content = process_content(section.content)
    else:
        sections = Section.objects.none()

    return render(request, 'search_results.html', {
        'sections': sections,
        'query': query,
        'products': products,
        'projects': projects,
        'products_sorted_by_product': products_sorted_by_product
    })


def get_unread_notifications_count(request):
    if request.user.is_authenticated:
        count = Notification.objects.filter(recipient=request.user, is_read=False).count()
        return JsonResponse({'count': count})
    else:
        return JsonResponse({'count': 0})


def search(query, objects, fields,):
    result = []
    query = str(query).lower()
    for obj in objects:
        for field in fields:
            value = str(getattr(obj, field)).lower()
            if query in value:
                result.append(obj)
    return result

