# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import phonenumber_field.modelfields
import location_field.models.plain


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Casteller',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('surname', models.CharField(max_length=50)),
                ('mail', models.EmailField(max_length=254, blank=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('location_name', models.CharField(max_length=50)),
                ('location', location_field.models.plain.PlainLocationField(max_length=63, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='type',
            field=models.ForeignKey(to='fortalesa.EventType'),
        ),
    ]
