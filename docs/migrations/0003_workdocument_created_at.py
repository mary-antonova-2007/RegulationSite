# Generated by Django 4.2.7 on 2023-11-22 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docs', '0002_alter_workdocument_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='workdocument',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата загрузки'),
        ),
    ]
