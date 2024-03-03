from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Task
from notification.models import Notification
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

@receiver(pre_save, sender=Task)
def task_pre_save(sender, instance, **kwargs):
    logger.info("task_pre_save signal triggered for Task")
    if instance.pk:
        old_task = Task.objects.get(pk=instance.pk)
        changed_fields = []
        for field in instance._meta.fields:
            field_name = field.name

            if field_name == 'status':
                old_value = Task.STATUS_DICT[getattr(old_task, field_name)]
                new_value = Task.STATUS_DICT[getattr(instance, field_name)]
            else:
                old_value = getattr(old_task, field_name)
                new_value = getattr(instance, field_name)

            if old_value != new_value:
                changed_fields.append(f"**{field.verbose_name}**: с *r*{old_value}*r* на **{new_value}**")

        if changed_fields:
            message = "\n".join(changed_fields)
            create_notifications_for_task(instance, message)

@receiver(post_save, sender=Task)
def task_post_save(sender, instance, created, **kwargs):
    logger.info("task_post_save signal triggered for Task")
    if created:
        create_notifications_for_task(instance, "Новая задача создана")

def create_notifications_for_task(task, message):
    # Создание уведомлений для подписчиков и ответственного пользователя
    users = set(list(task.subscribers.all()) + [task.responsible])
    for user in users:
        if user:  # Проверка, что пользователь не None
            Notification.objects.create(
                recipient=user,
                message=message,
                type='task_change',  # Пример типа уведомления
                from_user=User.objects.get(username='system'),  # Пример отправителя
                project=task.project,
                product=task.product,
                work_document=None  # Это поле необходимо установить соответствующим образом, если применимо
            )
