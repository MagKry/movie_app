# Generated by Django 3.0 on 2023-12-14 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homework_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='role',
        ),
        migrations.AddField(
            model_name='movie',
            name='year',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='personmovie',
            name='role',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
