# Generated by Django 5.1.1 on 2024-10-07 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_subscribed',
        ),
        migrations.AddField(
            model_name='user',
            name='wallet',
            field=models.IntegerField(default=0),
        ),
    ]
