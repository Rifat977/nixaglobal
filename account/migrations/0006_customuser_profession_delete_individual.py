# Generated by Django 5.0.3 on 2024-03-06 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_remove_company_company_name_customuser_company_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='profession',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Individual',
        ),
    ]
