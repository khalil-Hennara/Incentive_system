# Generated by Django 3.2 on 2021-08-16 10:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Employee', '0033_notification_user_notification'),
    ]

    operations = [
        migrations.CreateModel(
            name='Global_Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_read', models.BooleanField(default=True)),
                ('notification_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Employee.notification')),
            ],
        ),
    ]
