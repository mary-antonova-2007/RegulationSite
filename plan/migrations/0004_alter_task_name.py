# Generated by Django 4.2.7 on 2023-11-23 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0003_task_description_task_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='name',
            field=models.CharField(default=1, max_length=50, verbose_name='Название задачи'),
            preserve_default=False,
        ),
    ]
