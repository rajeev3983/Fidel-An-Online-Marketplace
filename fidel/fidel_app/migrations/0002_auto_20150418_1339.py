# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fidel_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='ad_attr',
            unique_together=set([('advertisement_id', 'attribute_id', 'ad_attr_value')]),
        ),
    ]
