# Generated by Django 3.2 on 2021-07-16 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employee', '0025_price_user_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
