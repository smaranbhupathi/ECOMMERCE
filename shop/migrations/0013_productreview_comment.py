# Generated by Django 5.0.2 on 2024-03-01 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_productreview'),
    ]

    operations = [
        migrations.AddField(
            model_name='productreview',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]
