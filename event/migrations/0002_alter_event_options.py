# Generated by Django 5.1 on 2024-08-09 03:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ('date',)},
        ),
    ]
