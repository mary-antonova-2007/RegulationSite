# Generated by Django 4.2.7 on 2023-11-18 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regulation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='footer',
            field=models.CharField(default='', max_length=200),
        ),
    ]