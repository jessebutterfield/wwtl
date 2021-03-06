# Generated by Django 3.2.2 on 2021-05-13 13:40

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
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=2)),
                ('zipcode', models.CharField(max_length=10)),
                ('home_phone', models.CharField(max_length=20)),
                ('work_phone', models.CharField(max_length=20)),
                ('cell_phone', models.CharField(max_length=20)),
                ('paper_mail', models.BooleanField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='league.player')),
            ],
        ),
        migrations.CreateModel(
            name='Singles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('division', models.IntegerField(choices=[(1, 'High Advanced'), (2, 'Advanced'), (3, 'High Intermediate'), (4, 'Intermediate'), (5, 'Low Intermediate'), (6, 'Beginner')])),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='league.season')),
            ],
        ),
        migrations.CreateModel(
            name='Doubles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('division', models.IntegerField(choices=[(1, 'High Advanced'), (2, 'Advanced'), (3, 'High Intermediate'), (4, 'Intermediate'), (5, 'Low Intermediate'), (6, 'Beginner')])),
                ('playerA', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='season_b', to='league.season')),
                ('playerB', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='season_a', to='league.season')),
            ],
        ),
    ]
