# Generated by Django 4.2.7 on 2023-11-23 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docs', '0005_room_room_designation_alter_room_room_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='room_designation',
            field=models.CharField(max_length=16, null=True, verbose_name='Обозначение комнаты'),
        ),
    ]
