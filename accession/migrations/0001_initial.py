# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-09 11:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_date_extensions.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('donor', '0001_initial'),
        ('controlled_list', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accession',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('seq', models.CharField(blank=True, max_length=10, null=True, unique=True)),
                ('title', models.CharField(max_length=300)),
                ('transfer_date', django_date_extensions.fields.ApproximateDateField()),
                ('description', models.TextField(blank=True, null=True)),
                ('access_note', models.TextField(blank=True, null=True)),
                ('module', models.IntegerField(blank=True, null=True)),
                ('row', models.IntegerField(blank=True, null=True)),
                ('section', models.IntegerField(blank=True, null=True)),
                ('shelf', models.IntegerField(blank=True, null=True)),
                ('creation_date_from', django_date_extensions.fields.ApproximateDateField(blank=True)),
                ('creation_date_to', django_date_extensions.fields.ApproximateDateField(blank=True)),
                ('custodial_history', models.TextField(blank=True, null=True)),
                ('copyright_note', models.TextField(blank=True, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('user_created', models.CharField(blank=True, max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('user_updated', models.CharField(blank=True, max_length=100)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
                ('user_approved', models.CharField(blank=True, max_length=100)),
                ('date_approved', models.DateTimeField(blank=True, null=True)),
                ('building', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='controlled_list.Building')),
            ],
            options={
                'db_table': 'accession_records',
            },
        ),
        migrations.CreateModel(
            name='AccessionCopyrightStatus',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(max_length=200, unique=True)),
            ],
            options={
                'db_table': 'accession_copyright_statuses',
                'ordering': ['status'],
            },
        ),
        migrations.CreateModel(
            name='AccessionItem',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('container', models.CharField(max_length=100)),
                ('content', models.CharField(blank=True, max_length=200, null=True)),
                ('accession', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accession.Accession')),
            ],
            options={
                'db_table': 'accession_items',
            },
        ),
        migrations.CreateModel(
            name='AccessionMethod',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('method', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'db_table': 'accession_methods',
                'ordering': ['method'],
            },
        ),
        migrations.AddField(
            model_name='accession',
            name='copyright_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='accession.AccessionCopyrightStatus'),
        ),
        migrations.AddField(
            model_name='accession',
            name='donor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='donor.Donor'),
        ),
        migrations.AddField(
            model_name='accession',
            name='method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accession.AccessionMethod'),
        ),
    ]
