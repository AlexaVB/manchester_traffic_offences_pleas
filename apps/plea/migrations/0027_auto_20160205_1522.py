# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plea', '0026_caseoffencefilter'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usagestats',
            old_name='postal_responses',
            new_name='postal_submissions',
        ),
        migrations.AddField(
            model_name='usagestats',
            name='postal_guilty_pleas',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='usagestats',
            name='postal_not_guilty_pleas',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='case',
            name='date_of_hearing',
            field=models.DateField(null=True, blank=True),
        ),
    ]
