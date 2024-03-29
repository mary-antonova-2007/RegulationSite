# Generated by Django 4.2.7 on 2023-11-23 18:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('docs', '0011_alter_product_description'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(verbose_name='Комментарий')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(verbose_name='Дата начала')),
                ('duration', models.IntegerField(verbose_name='Срок выполнения (дни)')),
                ('completion_date', models.DateField(blank=True, null=True, verbose_name='Дата выполнения')),
                ('status', models.CharField(choices=[('queued', 'В очереди'), ('in_progress', 'Выполняется'), ('completed', 'Завершено')], default='queued', max_length=20, verbose_name='Статус')),
                ('deadline', models.DateField(verbose_name='Дата дедлайна')),
                ('comments', models.ManyToManyField(blank=True, to='plan.comment', verbose_name='Комментарии')),
                ('document_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='docs.documenttype', verbose_name='Тип документа')),
                ('files', models.ManyToManyField(blank=True, to='docs.workdocument', verbose_name='Прикрепленные файлы')),
                ('predecessors', models.ManyToManyField(related_name='followed_by', to='plan.task', verbose_name='Предшественники')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='docs.product', verbose_name='Изделие')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='docs.project', verbose_name='Проект')),
                ('responsible', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='responsible_tasks', to=settings.AUTH_USER_MODEL, verbose_name='Ответственный')),
                ('subscribers', models.ManyToManyField(related_name='subscribed_tasks', to=settings.AUTH_USER_MODEL, verbose_name='Подписчики')),
            ],
        ),
    ]
