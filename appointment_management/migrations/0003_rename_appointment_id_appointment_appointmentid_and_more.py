# Generated by Django 5.1.4 on 2025-01-16 00:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appointment_management', '0002_rename_appointmentid_appointment_appointment_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='appointment_id',
            new_name='appointmentID',
        ),
        migrations.AlterModelTable(
            name='appointment',
            table=None,
        ),
    ]
