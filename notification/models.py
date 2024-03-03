from django.db import models
from django.contrib.auth.models import User
from docs.models import Project, Product, WorkDocument
from django.utils.translation import gettext_lazy as _


class Notification(models.Model):
    TYPE_CHOICES = (
        ('project_change', 'Изменение в проекте'),
        ('product_change', 'Изменение в изделии'),
        ('document_change', 'Изменение в документе'),
        ('document_add_to_project', 'Добавлен документ к проекту'),
        ('document_add_to_product', 'Добавлен документ к изделию'),
    )

    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_notifications',  # Уникальный related_name для отправителя
        verbose_name="Отправитель",
    )
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_notifications',  # Уникальный related_name для получателя
        verbose_name="Получатель"
    )
    message = models.TextField(_("сообщение"))
    type = models.CharField(max_length=30, choices=TYPE_CHOICES, verbose_name="Тип уведомления")
    is_read = models.BooleanField(default=False, verbose_name="Прочитано")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    # Связи с другими моделями
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications',
                                verbose_name="Проект")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications',
                                verbose_name="Продукт")
    work_document = models.ForeignKey(WorkDocument, on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='notifications', verbose_name="Рабочий документ")

    def __str__(self):
        return f"Уведомление для {self.recipient.username} о {self.get_type_display()}"

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"