# Generated by Django 3.1 on 2020-09-04 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0007_auto_20200904_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roster',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
