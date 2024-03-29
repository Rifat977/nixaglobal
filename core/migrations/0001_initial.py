# Generated by Django 5.0.3 on 2024-03-07 18:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='CommissionTier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foundation_commission', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('diploma_commission', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('bachelor_commission', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('masters_commission', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('phd_commission', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('research_based_commission', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('university', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.university')),
            ],
        ),
    ]
