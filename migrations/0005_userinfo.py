# Generated by Django 3.2.12 on 2022-03-24 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('integers', '0004_record_sensor_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, unique=True)),
            ],
        ),
    ]
