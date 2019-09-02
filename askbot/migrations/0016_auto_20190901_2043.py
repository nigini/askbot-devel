# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('askbot', '0015_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailfeedsetting',
            name='feed_type',
            field=models.CharField(max_length=16, choices=[(b'q_all', 'Entire forum'), (b'q_ask', 'Questions that I asked'), (b'q_ans', 'Questions that I answered'), (b'q_noans', 'Unanswered questions'), (b'q_sel', 'Individually selected questions'), (b'm_and_c', 'Mentions and comment responses')]),
        ),
    ]
