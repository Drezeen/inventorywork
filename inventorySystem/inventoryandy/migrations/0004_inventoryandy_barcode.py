# Generated by Django 5.0.1 on 2024-02-16 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventoryandy', '0003_alter_inventoryandy_remaining_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryandy',
            name='barcode',
            field=models.CharField(blank=True, max_length=100, unique=True),
        ),
    ]