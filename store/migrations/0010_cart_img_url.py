# Generated by Django 3.1.6 on 2021-11-27 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_comment_product_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='img_url',
            field=models.CharField(default='img/Featured/danchou_tshirt.png', max_length=1000),
        ),
    ]
