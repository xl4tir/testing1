# Generated by Django 3.1.3 on 2020-12-03 20:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0012_auto_20201203_2153'),
    ]

    operations = [
        migrations.AddField(
            model_name='test_complete',
            name='testname',
            field=models.CharField(default=' ', max_length=200, verbose_name='Назва тесту'),
        ),
        migrations.AlterField(
            model_name='test_complete',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 3, 22, 21, 13, 292857), verbose_name='Дата проходження тесту'),
        ),
        migrations.AlterField(
            model_name='tests_complete',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 3, 22, 21, 13, 291831), verbose_name='Дата проходження тесту'),
        ),
    ]
