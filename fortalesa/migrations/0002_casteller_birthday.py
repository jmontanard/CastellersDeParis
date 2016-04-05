# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fortalesa', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='casteller',
            name='birthday',
            field=models.DateField(default=None),
            preserve_default=False,
        ),
    ]
