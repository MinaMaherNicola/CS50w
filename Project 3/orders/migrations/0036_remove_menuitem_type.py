# Generated by Django 2.0.3 on 2018-09-03 19:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0035_auto_20180903_1435'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menuitem',
            name='type',
        ),
    ]
