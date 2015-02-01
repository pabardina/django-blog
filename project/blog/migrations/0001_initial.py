# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.CharField(max_length=30, unique=True)),
                ('short_content', models.CharField(max_length=250)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('published', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-created_at'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='article',
            name='categories',
            field=models.ManyToManyField(to='blog.Category', blank=True, null=True),
            preserve_default=True,
        ),
    ]
