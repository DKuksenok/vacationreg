# Generated by Django 3.0.6 on 2020-05-19 17:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registry', '0004_auto_20200515_1544'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='date_dismissal',
            new_name='dismissal_date',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='is_dismissal',
        ),
    ]
