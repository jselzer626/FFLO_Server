# Generated by Django 3.1 on 2020-08-18 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0002_player_ffnid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='profileImg',
            field=models.CharField(max_length=150),
        ),
    ]
