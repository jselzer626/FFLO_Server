# Generated by Django 3.1 on 2020-08-18 19:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Roster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=20)),
                ('lname', models.CharField(max_length=20)),
                ('displayName', models.CharField(max_length=40)),
                ('position', models.CharField(max_length=3)),
                ('team', models.CharField(max_length=3)),
                ('ranking', models.IntegerField(default=999)),
                ('profileImg', models.CharField(max_length=100)),
                ('roster', models.ManyToManyField(blank=True, to='players.Roster')),
            ],
        ),
    ]
