# Generated by Django 3.1.7 on 2021-03-21 21:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mult', '0005_auto_20210321_2102'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeriesFilms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_serie', models.TextField(verbose_name='Название серии')),
                ('href', models.TextField(verbose_name='Ссылка на серию')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mult.film')),
            ],
            options={
                'verbose_name': 'Серия',
                'verbose_name_plural': 'Серии',
                'ordering': ['name_serie'],
            },
        ),
    ]
