# Generated by Django 5.1.4 on 2025-01-21 22:52

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_rename_email_loginsignup_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='loginsignup',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
