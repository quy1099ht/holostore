# Generated by Django 3.1.6 on 2021-11-20 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_auto_20211120_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(default='Quy', max_length=255),
        ),
    ]
