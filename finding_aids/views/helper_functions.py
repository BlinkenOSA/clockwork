from container.models import Container
from finding_aids.models import FindingAidsEntity


def get_number_of_folders(container_id):
    return FindingAidsEntity.objects.filter(container=Container.objects.get(pk=container_id))\
                                    .values('folder_no').distinct().count()


def get_number_of_items(container_id, folder_no):
    return FindingAidsEntity.objects.filter(level='I')\
        .filter(container=Container.objects.get(pk=container_id))\
        .filter(folder_no=folder_no)\
        .count()


def new_number(new_obj):
    if new_obj.level == 'F':
        return {'folder_no': new_obj.folder_no + 1, 'sequence_no': 0}
    else:
        return {'folder_no': new_obj.folder_no, 'sequence_no': new_obj.sequence_no + 1}


def renumber_entries(action, fa_entity):
    if action == 'delete':
        step = -1
    else:
        step = 1

    if fa_entity.level == 'F':
        folders = FindingAidsEntity.objects.filter(container=fa_entity.container,
                                                   folder_no__gt=fa_entity.folder_no)
        for folder in folders:
            folder.folder_no += step
            folder.save()
    else:
        items = FindingAidsEntity.objects.filter(container=fa_entity.container,
                                                 level=fa_entity.level,
                                                 folder_no=fa_entity.folder_no,
                                                 sequence_no__gt=fa_entity.sequence_no)
        if len(items) > 0:
            for item in items:
                item.sequence_no += step
                item.save()
        else:
            folders = FindingAidsEntity.objects.filter(container=fa_entity.container,
                                                       level=fa_entity.level,
                                                       folder_no__gt=fa_entity.folder_no)
            for folder in folders:
                folder.folder_no += step
                folder.save()
