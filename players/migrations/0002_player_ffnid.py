# Generated by Django 3.1 on 2020-08-18 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='ffnId',
            field=models.IntegerField(default=999),
        ),
    ]