# Generated by Django 4.2.7 on 2023-11-23 09:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('docs', '0008_alter_product_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='docs.room', verbose_name='Помещение'),
        ),
    ]