# Generated by Django 4.2.3 on 2023-07-17 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.CharField(max_length=50)),
                ('text', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('answer_time', models.DurationField()),
                ('status', models.IntegerField(choices=[(1, 'Pending'), (2, 'Sent'), (3, 'Error')], default=1, verbose_name='Статус')),
            ],
        ),
    ]
