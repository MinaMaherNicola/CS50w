# Generated by Django 2.0.3 on 2018-09-03 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0026_auto_20180903_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='type',
            field=models.CharField(choices=[('PZ', 'Pizza'), ('SB', 'Subs'), ('PA', 'Pasta'), ('SA', 'Salad'), ('DP', 'Dinner Platters')], max_length=2),
        ),
    ]
