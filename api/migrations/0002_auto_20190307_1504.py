# Generated by Django 2.1.7 on 2019-03-07 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wechatuser',
            name='city',
        ),
        migrations.RemoveField(
            model_name='wechatuser',
            name='province',
        ),
        migrations.AlterField(
            model_name='wechatuser',
            name='openid',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
