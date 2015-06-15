# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LikePost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('ip', models.IPAddressField()),
                ('article', models.ForeignKey(to='blog.Article')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
