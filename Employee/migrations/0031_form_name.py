# Generated by Django 3.2 on 2021-08-16 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employee', '0030_auto_20210816_0818'),
    ]

    operations = [
        migrations.AddField(
            model_name='form',
            name='name',
            field=models.CharField(max_length=30, null=True),
        ),
    ]