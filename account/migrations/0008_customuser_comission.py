# Generated by Django 5.0.3 on 2024-03-07 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_alter_customuser_company_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='comission',
            field=models.FloatField(default=0.0),
        ),
    ]
