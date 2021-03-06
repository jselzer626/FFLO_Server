# Generated by Django 3.1 on 2020-09-02 23:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0005_auto_20200818_1636'),
    ]

    operations = [
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=10)),
                ('verify', models.CharField(max_length=7)),
            ],
        ),
        migrations.AlterField(
            model_name='roster',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='players.owner'),
        ),
    ]
