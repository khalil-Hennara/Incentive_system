# Generated by Django 3.2 on 2021-06-09 11:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Employee', '0023_rate'),
    ]

    operations = [
        migrations.CreateModel(
            name='user_rate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('note', models.CharField(max_length=200, null=True)),
                ('value', models.IntegerField()),
                ('Rate_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Employee.rate')),
                ('employee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Employee.employee')),
            ],
        ),
        migrations.RemoveField(
            model_name='user_permession',
            name='permession_id',
        ),
        migrations.AlterField(
            model_name='user_permession',
            name='Rate_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Employee.rate'),
        ),
        migrations.DeleteModel(
            name='Permessions',
        ),
    ]
