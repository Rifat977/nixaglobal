# Generated by Django 5.0.3 on 2024-03-12 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_applicationstatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='commissiontier',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]