# Generated by Django 5.1.4 on 2025-01-12 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loginsignup',
            name='Email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='loginsignup',
            name='MobileNumber',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='loginsignup',
            name='UserName',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
