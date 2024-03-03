from django.contrib.auth.models import User
from django.db import models
from docs.models import Project, Product, WorkDocument, DocumentType


# Create your models here.
class Task(models.Model):
    STATUS_CHOICES = [
        ('queued', 'В очереди'),
        ('in_progress', 'Выполняется'),
        ('completed', 'Завершено'),
    ]
    STATUS_DICT = dict(STATUS_CHOICES)
    name = models.CharField(max_length=50, verbose_name="Название задачи", null=True, blank=True)
    description = models.TextField(max_length=200, verbose_name="Описание задачи", null=True, blank=True)
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE, verbose_name="Проект", null=True, blank=True)
    product = models.ForeignKey(Product, related_name='tasks', on_delete=models.CASCADE, verbose_name="Изделие", null=True, blank=True)
    document_type = models.ForeignKey(DocumentType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Тип документа")
    subscribers = models.ManyToManyField(User, related_name='subscribed_tasks', verbose_name="Подписчики")
    responsible = models.ForeignKey(User, related_name='responsible_tasks', on_delete=models.SET_NULL, null=True, verbose_name="Ответственный", blank=True)
    start_date = models.DateField(verbose_name="Дата начала")
    duration = models.IntegerField(verbose_name="Срок выполнения (дни)")
    completion_date = models.DateField(null=True, blank=True, verbose_name="Дата выполнения")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='queued', verbose_name="Статус")
    deadline = models.DateField(verbose_name="Дата дедлайна")
    predecessors = models.ManyToManyField('self', symmetrical=False, related_name='followed_by', verbose_name="Предшественники", blank=True)
    files = models.ManyToManyField(WorkDocument, verbose_name="Прикрепленные файлы", blank=True)
    comments = models.ManyToManyField('Comment', verbose_name="Комментарии", blank=True)

    def __str__(self):
        text = 'Задача: '
        if self.project:
            text += self.project.name
        elif self.product:
            text += self.product.project.name
        if self.product:
            text += f' по изделию {self.product.name} '
        text += ' ' + self.name
        return text


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    comment = models.TextField(verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f'Комментарий от {self.user.username} ({self.created_at})'