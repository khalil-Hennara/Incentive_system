# Generated by Django 3.2 on 2021-08-16 08:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Employee', '0031_form_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_rate_form',
            name='Form_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Employee.form'),
        ),
    ]