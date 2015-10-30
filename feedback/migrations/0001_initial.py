# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FeedbackEmail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, null=True, verbose_name="Receiver's name", blank=True)),
                ('email', models.EmailField(max_length=200, verbose_name='Email')),
            ],
            options={
                'verbose_name': 'Email address',
                'verbose_name_plural': 'Email addresses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MailingList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, null=True, verbose_name='List title')),
                ('form', models.CharField(unique=True, max_length=100, verbose_name='Feedback form', choices=[(b'default', b'Default'), (b'email_us', '\u0424\u043e\u0440\u043c\u0430 \u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u044f \u0441 \u0441\u0430\u0439\u0442\u0430')])),
                ('default_from', models.EmailField(max_length=200, null=True, verbose_name='Default sender email', blank=True)),
                ('emails', models.ManyToManyField(related_name='forms', verbose_name='List of addresses', to='feedback.FeedbackEmail', blank=True)),
            ],
            options={
                'verbose_name': 'Mailing list',
                'verbose_name_plural': 'Mailing lists',
            },
            bases=(models.Model,),
        ),
    ]
