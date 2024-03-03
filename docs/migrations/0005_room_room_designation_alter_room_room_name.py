# Generated by Django 4.2.7 on 2023-11-23 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docs', '0004_remove_product_room_name_room_product_room'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='room_designation',
            field=models.CharField(default=1, max_length=16, verbose_name='Обозначение комнаты'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='room',
            name='room_name',
            field=models.CharField(max_length=50, verbose_name='Название комнаты'),
        ),
    ]
