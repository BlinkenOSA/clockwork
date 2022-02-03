import pysolr
from celery.task import task
from django.conf import settings

from isad.indexer import ISADIndexer


@task(name="index_add_isad")
def index_add_isad(isad_id):
    solr_core = getattr(settings, "SOLR_ADDRESS", "http://localhost:8983/solr/osacatalog")
    solr_interface = pysolr.Solr(solr_core)
    indexer = ISADIndexer(isad_id=isad_id)
    indexer.prepare_index()
    solr_interface.add([indexer.solr_document], commit=True)


@task(name="index_remove_isad")
def index_remove_isad(isad_id):
    solr_core = getattr(settings, "SOLR_ADDRESS", "http://localhost:8983/solr/osacatalog")
    solr_interface = pysolr.Solr(solr_core)
    indexer = ISADIndexer(isad_id=isad_id)
    solr_interface.delete(id=indexer.get_solr_id())
