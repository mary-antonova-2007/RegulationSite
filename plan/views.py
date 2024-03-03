from django.shortcuts import render, get_object_or_404, redirect
from .forms import TaskForm
from docs.models import Project, Product
from django.http import JsonResponse
from .models import Task

def add_task(request, project_id=None, product_id=None):
    project = None
    product = None

    if project_id:
        project = get_object_or_404(Project, pk=project_id)
    elif product_id:
        product = get_object_or_404(Product, pk=product_id)
        project = product.project

    if request.method == 'POST':
        form = TaskForm(request.POST, project=project, product=product)
        if form.is_valid():
            task = form.save(commit=False)
            if project:
                task.project = project
            if product:
                task.product = product
            task.save()
            form.save_m2m()  # Сохранение ManyToMany полей
            return redirect('index')  # Перенаправление после создания задачи
    else:
        form = TaskForm(project=project, product=product)

    return render(request, 'plan/add_task.html', {'form': form})

from django.shortcuts import render
from .models import Task
from django.http import JsonResponse
from datetime import datetime

def gantt_chart_view(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        tasks = Task.objects.filter(
            start_date__gte=datetime.strptime(start_date, '%Y-%m-%d'),
            deadline__lte=datetime.strptime(end_date, '%Y-%m-%d')
        )
    else:
        tasks = Task.objects.all()

    # Преобразование данных задач для диаграммы Ганта
    gantt_data = [
        {
            'id': str(task.id),
            'name': f'{task.product} - {task.name}',
            'start': task.start_date.strftime("%Y-%m-%d") if task.start_date else None,
            'end': task.deadline.strftime("%Y-%m-%d") if task.deadline else None,
            'dependencies': ','.join(str(predecessor.id) for predecessor in task.predecessors.all())
            # Добавьте другие необходимые поля
        } for task in tasks
    ]

    return render(request, 'plan/gantt_chart.html', {'gantt_data': gantt_data})

def load_products(request):
    project_id = request.GET.get('project_id')
    products = Product.objects.filter(project_id=project_id).order_by('name')
    products_data = [{'id': product.id, 'name': str(product)} for product in products]
    return JsonResponse(products_data, safe=False)


def load_predecessors(request):
    project_id = request.GET.get('project_id')
    tasks = Task.objects.filter(project_id=project_id).exclude(status='completed').order_by('name')
    tasks_data = [{'id': task.id, 'name': str(task)} for task in tasks]
    return JsonResponse(tasks_data, safe=False)
