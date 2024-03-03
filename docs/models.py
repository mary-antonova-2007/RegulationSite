import os
import threading

from shutil import copy2

from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    project_manager = models.ForeignKey(User, related_name='managed_projects', on_delete=models.SET_NULL, null=True, verbose_name="Менеджер проекта")
    project_designer = models.ForeignKey(User, related_name='designed_projects', on_delete=models.SET_NULL, null=True, verbose_name="Дизайнер проекта")
    designation = models.CharField(max_length=100, verbose_name="Обозначение")
    path_to_project_folder = models.CharField(max_length=255, verbose_name="Путь к папке для сохранения", blank=True)

    def __str__(self):
        return f'{self.name} - Договор № {self.designation}'

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"


class Room(models.Model):
    room_designation = models.CharField(max_length=16, verbose_name="Обозначение комнаты", null=True)
    room_name = models.CharField(max_length=50, verbose_name="Название комнаты", null=True)
    project = models.ForeignKey(Project, related_name='rooms', on_delete=models.CASCADE, verbose_name="Проект")

    def __str__(self):
        return f'{self.room_designation} - {self.room_name}'

    class Meta:
        verbose_name = "Помещение"
        verbose_name_plural = "Помещения"


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    project = models.ForeignKey(Project, related_name='products', on_delete=models.CASCADE, verbose_name="Проект")
    product_designer = models.ForeignKey(User, related_name='designed_products', on_delete=models.SET_NULL, null=True, verbose_name="Дизайнер продукта")
    designation = models.CharField(max_length=30, verbose_name="Обозначение")
    room = models.ForeignKey(Room, related_name='products', on_delete=models.SET_NULL, null=True, verbose_name="Помещение", blank=True)
    description = models.description = models.TextField(max_length=300, verbose_name="Информация", blank=True, null=True)

    def __str__(self):
        return f'{self.name} - {self.room}'

    class Meta:
        verbose_name = "Изделие"
        verbose_name_plural = "Изделия"


class DocumentType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    isSingleton = models.BooleanField(default=False, verbose_name="Единственный экземпляр")
    sub_folder = models.CharField(max_length=255, verbose_name="Путь к папке для сохранения", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип документа"
        verbose_name_plural = "Типы документов"


class WorkDocument(models.Model):
    name = models.CharField(max_length=300, verbose_name="Название")
    content = models.FileField(max_length=300, upload_to='documents/', verbose_name="Файл")
    product = models.ForeignKey(Product, related_name='documents', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Изделие")
    project = models.ForeignKey(Project, related_name='documents', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Проект")
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE, verbose_name="Тип документа")
    isArchived = models.BooleanField(default=False, verbose_name="Архивирован")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки", null=True)
    path_to_backup = models.CharField(max_length=300, verbose_name="Путь к backup файлу", blank=True)
    backup_saved = models.BooleanField(default=False, verbose_name="Backup сохранен")

    def backup_save(self, *args, **kwargs):
        """Выполняет резервное копирование файла."""
        self.path_to_backup = self.get_full_path()
        if os.path.exists(self.project.path_to_project_folder):
            if self.path_to_backup:
                # Создаем все необходимые директории, если они не существуют
                os.makedirs(os.path.dirname(self.path_to_backup), exist_ok=True)
                # Копируем файл
                copy2(self.content.path, self.path_to_backup)
                self.backup_saved = True
            else:
                self.backup_saved = False
        super(WorkDocument, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.product:
            self.project = self.product.project
        if self.document_type.isSingleton:
            # Пометить существующие документы того же типа как архивные
            existing_docs = WorkDocument.objects.filter(
                document_type=self.document_type,
                isArchived=False
            )
            if existing_docs:
                if self.product:
                    existing_docs = existing_docs.filter(product=self.product)
                elif self.project:
                    existing_docs = existing_docs.filter(project=self.project)

                existing_docs.update(isArchived=True)
        super(WorkDocument, self).save(*args, **kwargs)

    def get_full_path(self):
        """Возвращает полный путь для резервного копирования."""
        base_path = self.project.path_to_project_folder if self.project else self.product.project.path_to_project_folder
        sub_folder = self.document_type.sub_folder if self.document_type else ''
        product_folder = f"{self.product.name} {self.product.designation}" if self.product else ''

        return os.path.join(base_path, sub_folder, product_folder, os.path.basename(self.content.name))

    def start_backup(self):
        """Запускает асинхронную проверку пути и резервное копирование."""
        thread = threading.Thread(target=self.backup_save)
        print('start backup')
        thread.start()
        print('end thread backup')


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Рабочий документ"
        verbose_name_plural = "Рабочие документы"


