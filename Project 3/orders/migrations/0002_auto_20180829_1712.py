# Generated by Django 2.0.3 on 2018-08-29 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pizza',
            name='size',
        ),
        migrations.AddField(
            model_name='menuitem',
            name='size',
            field=models.CharField(blank=True, choices=[('S', 'Small'), ('L', 'Large'), ('', 'Not Applicable')], max_length=1),
        ),
    ]
