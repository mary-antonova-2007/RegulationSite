# Generated by Django 4.2.7 on 2023-11-23 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docs', '0006_alter_room_room_designation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='room_name',
            field=models.CharField(max_length=50, null=True, verbose_name='Название комнаты'),
        ),
    ]
