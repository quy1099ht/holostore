# Generated by Django 3.1.6 on 2021-11-17 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_product_tag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='start_date',
        ),
        migrations.AlterField(
            model_name='cart',
            name='ordered_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
