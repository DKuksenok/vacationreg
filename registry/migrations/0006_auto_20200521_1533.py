# Generated by Django 3.0.6 on 2020-05-21 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registry', '0005_auto_20200519_2057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='middle_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='отчество'),
        ),
    ]
