# Generated by Django 3.1 on 2020-09-04 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0008_auto_20200904_1323'),
    ]

    operations = [
        migrations.AddField(
            model_name='roster',
            name='parameters',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
