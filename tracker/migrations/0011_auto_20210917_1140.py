# Generated by Django 3.1.12 on 2021-09-17 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0010_item_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='joindate',
        ),
        migrations.AlterField(
            model_name='item',
            name='created_at',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
