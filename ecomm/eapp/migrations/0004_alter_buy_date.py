# Generated by Django 5.1.3 on 2024-11-20 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eapp', '0003_buy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buy',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]