# Generated by Django 3.2.2 on 2021-07-25 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0004_auto_20210725_0100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doubleset',
            name='away',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='doubleset',
            name='home',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='singleset',
            name='away',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='singleset',
            name='home',
            field=models.IntegerField(null=True),
        ),
    ]
