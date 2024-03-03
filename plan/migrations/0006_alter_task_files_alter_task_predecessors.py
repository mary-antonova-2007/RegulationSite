# Generated by Django 4.2.7 on 2023-11-28 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docs', '0011_alter_product_description'),
        ('plan', '0005_alter_task_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='files',
            field=models.ManyToManyField(blank=True, to='docs.workdocument', verbose_name='Прикрепленные файлы'),
        ),
        migrations.AlterField(
            model_name='task',
            name='predecessors',
            field=models.ManyToManyField(blank=True, related_name='followed_by', to='plan.task', verbose_name='Предшественники'),
        ),
    ]
