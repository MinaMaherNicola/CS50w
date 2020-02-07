# Generated by Django 2.0.3 on 2018-08-30 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_auto_20180830_1054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='crust',
            field=models.CharField(blank=True, choices=[('S', 'Sicilian'), ('R', 'Regular'), ('', '')], default='', max_length=1),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='size',
            field=models.CharField(blank=True, choices=[('S', 'Small'), ('L', 'Large'), ('', '')], max_length=1),
        ),
    ]
