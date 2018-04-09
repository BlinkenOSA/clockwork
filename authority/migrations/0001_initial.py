# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-09 11:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Corporation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250, unique=True)),
                ('wiki_url', models.CharField(blank=True, max_length=150, null=True)),
                ('authority_url', models.CharField(blank=True, max_length=150, null=True)),
                ('other_url', models.CharField(blank=True, max_length=150, null=True)),
                ('user_created', models.CharField(blank=True, max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('user_updated', models.CharField(blank=True, max_length=100)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'db_table': 'authority_corporations',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='CorporationOtherFormat',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250, unique=True)),
                ('corporation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authority.Corporation')),
            ],
            options={
                'db_table': 'authority_corporations_other_formats',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('alpha2', models.CharField(blank=True, max_length=2, null=True)),
                ('alpha3', models.CharField(max_length=3)),
                ('wiki_url', models.CharField(blank=True, max_length=150, null=True)),
                ('authority_url', models.CharField(blank=True, max_length=200, null=True)),
                ('country', models.CharField(max_length=100, unique=True)),
                ('user_created', models.CharField(blank=True, max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('user_updated', models.CharField(blank=True, max_length=100)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'db_table': 'authority_countries',
                'ordering': ['country'],
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('genre', models.CharField(max_length=50, unique=True)),
                ('wiki_url', models.CharField(blank=True, max_length=150, null=True)),
                ('authority_url', models.CharField(blank=True, max_length=150, null=True)),
                ('other_url', models.CharField(blank=True, max_length=150, null=True)),
                ('user_created', models.CharField(blank=True, max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('user_updated', models.CharField(blank=True, max_length=100)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'db_table': 'authority_genres',
                'ordering': ['genre'],
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('iso_639_1', models.CharField(blank=True, max_length=10, null=True)),
                ('iso_639_2', models.CharField(blank=True, max_length=10, null=True)),
                ('wiki_url', models.CharField(blank=True, max_length=150, null=True)),
                ('authority_url', models.CharField(blank=True, max_length=200, null=True)),
                ('language', models.CharField(max_length=100, unique=True)),
                ('user_created', models.CharField(blank=True, max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('user_updated', models.CharField(blank=True, max_length=100)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'db_table': 'authority_languages',
                'ordering': ['language'],
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('wiki_url', models.CharField(blank=True, max_length=150, null=True)),
                ('authority_url', models.CharField(blank=True, max_length=150, null=True)),
                ('other_url', models.CharField(blank=True, max_length=150, null=True)),
                ('user_created', models.CharField(blank=True, max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('user_updated', models.CharField(blank=True, max_length=100)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'db_table': 'authority_people',
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.CreateModel(
            name='PersonOtherFormat',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('language', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='authority.Language')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authority.Person')),
            ],
            options={
                'db_table': 'authority_people_other_formats',
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('wiki_url', models.CharField(blank=True, max_length=150, null=True)),
                ('authority_url', models.CharField(blank=True, max_length=200, null=True)),
                ('place', models.CharField(max_length=100, unique=True)),
                ('other_url', models.CharField(blank=True, max_length=150, null=True)),
                ('user_created', models.CharField(blank=True, max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('user_updated', models.CharField(blank=True, max_length=100)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'db_table': 'authority_places',
                'ordering': ['place'],
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('subject', models.CharField(max_length=50, unique=True)),
                ('wiki_url', models.CharField(blank=True, max_length=150, null=True)),
                ('authority_url', models.CharField(blank=True, max_length=150, null=True)),
                ('other_url', models.CharField(blank=True, max_length=150, null=True)),
                ('user_created', models.CharField(blank=True, max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('user_updated', models.CharField(blank=True, max_length=100)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'db_table': 'authority_subjects',
                'ordering': ['subject'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='person',
            unique_together=set([('last_name', 'first_name')]),
        ),
        migrations.AlterUniqueTogether(
            name='language',
            unique_together=set([('iso_639_1', 'iso_639_2')]),
        ),
        migrations.AddField(
            model_name='corporationotherformat',
            name='language',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='authority.Language'),
        ),
        migrations.AlterUniqueTogether(
            name='personotherformat',
            unique_together=set([('last_name', 'first_name')]),
        ),
    ]
