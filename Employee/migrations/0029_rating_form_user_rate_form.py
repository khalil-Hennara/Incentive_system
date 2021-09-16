# Generated by Django 3.2 on 2021-08-16 07:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Employee', '0028_complaint_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating_Form',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hours_expire', models.IntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('Rate_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Employee.rate')),
            ],
        ),
        migrations.CreateModel(
            name='User_Rate_Form',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('Form_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Employee.rating_form')),
                ('employee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Employee.employee')),
            ],
        ),
    ]