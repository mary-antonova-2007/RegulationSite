# Generated by Django 4.2.7 on 2023-11-23 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0002_alter_task_files_alter_task_predecessors'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='description',
            field=models.TextField(blank=True, max_length=200, null=True, verbose_name='Описание задачи'),
        ),
        migrations.AddField(
            model_name='task',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Название задачи'),
        ),
    ]