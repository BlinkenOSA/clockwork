import pysolr
from celery.task import task

from django.conf import settings

from finding_aids.indexer import FindingAidsEntityIndexer
from finding_aids.models import FindingAidsEntity


@task(name="index_add_finding_aids")
def index_add_finding_aids(finding_aids_entity_id):
    solr_core = getattr(settings, "SOLR_ADDRESS", "http://localhost:8983/solr/osacatalog")
    solr_interface = pysolr.Solr(solr_core)
    finding_aids = FindingAidsEntity.objects.get(pk=finding_aids_entity_id)
    indexer = FindingAidsEntityIndexer(finding_aids_entity_id=finding_aids.id)
    indexer.prepare_index()
    solr_interface.add([indexer.solr_document], commit=True)


@task(name="index_add_finding_aids_confidential")
def index_add_finding_aids_confidential(finding_aids_entity_id):
    solr_core = getattr(settings, "SOLR_ADDRESS", "http://localhost:8983/solr/osacatalog")
    solr_interface = pysolr.Solr(solr_core)
    finding_aids = FindingAidsEntity.objects.get(pk=finding_aids_entity_id)
    indexer = FindingAidsEntityIndexer(finding_aids_entity_id=finding_aids.id)
    indexer.prepare_confidential_index()
    solr_interface.add([indexer.solr_document], commit=True)


@task(name="index_remove_finding_aids")
def index_remove_finding_aids(finding_aids_entity_id):
    solr_core = getattr(settings, "SOLR_ADDRESS", "http://localhost:8983/solr/osacatalog")
    solr_interface = pysolr.Solr(solr_core)
    finding_aids = FindingAidsEntity.objects.get(pk=finding_aids_entity_id)
    indexer = FindingAidsEntityIndexer(finding_aids_entity_id=finding_aids.id)
    solr_interface.delete(id=indexer.get_solr_id(), commit=True)
