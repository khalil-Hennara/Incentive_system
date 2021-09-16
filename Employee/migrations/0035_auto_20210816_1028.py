# Generated by Django 3.2 on 2021-08-16 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employee', '0034_global_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='global_notification',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user_notification',
            name='is_read',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
