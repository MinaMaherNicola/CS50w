# Generated by Django 2.0.3 on 2018-08-30 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0015_auto_20180830_1737'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='item',
        ),
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(blank=True, related_name='orders', to='orders.MenuItem'),
        ),
    ]
