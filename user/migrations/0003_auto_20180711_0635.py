# Generated by Django 2.0.3 on 2018-07-11 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20180710_0840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='contact',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
    ]
