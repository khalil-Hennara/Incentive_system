# Generated by Django 3.2 on 2021-06-09 10:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Employee', '0021_auto_20210609_1031'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permessions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permession_name', models.CharField(max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='user_permession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expire_time', models.DateTimeField()),
                ('Rate_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Employee.rating')),
                ('employee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Employee.employee')),
                ('permession_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Employee.permessions')),
            ],
        ),
        migrations.RemoveField(
            model_name='user_rate',
            name='Rate_id',
        ),
        migrations.RemoveField(
            model_name='user_rate',
            name='employee_id',
        ),
        migrations.DeleteModel(
            name='Rate',
        ),
        migrations.DeleteModel(
            name='user_rate',
        ),
    ]
