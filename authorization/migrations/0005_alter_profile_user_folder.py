# Generated by Django 4.2.7 on 2023-11-28 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0004_alter_profile_birth_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user_folder',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
