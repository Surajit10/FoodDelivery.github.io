# Generated by Django 3.1.7 on 2021-04-13 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0006_remove_ordermodel_is_shipped'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordermodel',
            name='is_shipped',
            field=models.BooleanField(default=False),
        ),
    ]
