#!/usr/bin/env bash
rm ./*/migrations/00*.py
rm ./*/migrations/00*.pyc

python ./manage.py flush
python ./manage.py makemigrations
python ./manage.py migrate

python ./manage.py loaddata --app accession accession_copyright_status.yaml
python ./manage.py loaddata --app accession accession_method.yaml
python ./manage.py loaddata --app authority country.yaml
python ./manage.py loaddata --app authority language.yaml
python ./manage.py loaddata --app controlled_list access_rights.yaml
python ./manage.py loaddata --app controlled_list archival_unit_theme.yaml
python ./manage.py loaddata --app controlled_list building.yaml
python ./manage.py loaddata --app controlled_list carrier_type.yaml
python ./manage.py loaddata --app controlled_list date_type.yaml
python ./manage.py loaddata --app controlled_list extent_unit.yaml
python ./manage.py loaddata --app controlled_list language_usage.yaml
python ./manage.py loaddata --app controlled_list locale.yaml
python ./manage.py loaddata --app controlled_list primary_type.yaml
python ./manage.py loaddata --app controlled_list reproduction_rights.yaml
python ./manage.py loaddata --app controlled_list rights_restriction_reason.yaml

python ./manage.py creategroups

python ./manage.py migrateusers
python ./manage.py migrateaccessions
python ./manage.py migratedonors
python ./manage.py migratearchivalunits
python ./manage.py migrateisaars
python ./manage.py migrateisads
python ./manage.py migratecontainers
python ./manage.py migratecontentstxt
python ./manage.py migratecontentsav
