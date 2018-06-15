import pysolr
from celery.task import task
from isad.indexer import ISADIndexer


@task(name="index_add_isad")
def index_add_isad(isad_id):
    solr_interface = pysolr.Solr("http://localhost:8983/solr/osacatalog")
    indexer = ISADIndexer(isad_id=isad_id)
    indexer.prepare_index()
    solr_interface.add([indexer.solr_document], commit=True)


@task(name="index_remove_isad")
def index_remove_isad(isad_id):
    solr_interface = pysolr.Solr("http://localhost:8983/solr/osacatalog")
    indexer = ISADIndexer(isad_id=isad_id)
    solr_interface.delete(id=indexer.get_solr_id())
