# Generated by Django 3.2 on 2021-04-17 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employee', '0015_alter_rating_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='note',
            field=models.CharField(max_length=200),
        ),
    ]
