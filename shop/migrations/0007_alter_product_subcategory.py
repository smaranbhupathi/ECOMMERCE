# Generated by Django 5.0.1 on 2024-02-06 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_orderupdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='subcategory',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
