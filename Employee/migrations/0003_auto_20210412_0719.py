# Generated by Django 3.2 on 2021-04-12 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employee', '0002_alter_employee_phone_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='boss_id',
        ),
        migrations.AddField(
            model_name='employee',
            name='boss_id',
            field=models.ManyToManyField(to='Employee.Employee'),
        ),
    ]
