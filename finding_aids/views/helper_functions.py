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
    if new_obj.description_level == 'L1':
        return {'folder_no': new_obj.folder_no + 1, 'sequence_no': 0}
    else:
        return {'folder_no': new_obj.folder_no, 'sequence_no': new_obj.sequence_no + 1}


def renumber_entries(action, fa_entity):
    # L1 entities
    if fa_entity.description_level == 'L1':
        folders = FindingAidsEntity.objects.filter(container=fa_entity.container,
                                                   folder_no__gt=fa_entity.folder_no)

        # Delete L1 entities
        if action == 'delete':
            item_count = FindingAidsEntity.objects.filter(container=fa_entity.container,
                                                          description_level='L2',
                                                          folder_no=fa_entity.folder_no).count()
            if item_count == 0:
                for folder in folders:
                    folder.folder_no -= 1
                    folder.save()

        # Clone L1 entities
        else:
            for folder in folders:
                folder.folder_no += 1
                folder.save()

    # L2 entities
    else:
        folders = FindingAidsEntity.objects.filter(container=fa_entity.container,
                                                   folder_no__gt=fa_entity.folder_no)
        items = FindingAidsEntity.objects.filter(container=fa_entity.container,
                                                 level=fa_entity.level,
                                                 folder_no=fa_entity.folder_no,
                                                 sequence_no__gt=fa_entity.sequence_no)

        # Delete entities
        if action == 'delete':
            item_count = FindingAidsEntity.objects.filter(container=fa_entity.container,
                                                          description_level='L2',
                                                          folder_no=fa_entity.folder_no).count()
            if item_count == 0:
                for folder in folders:
                    folder.folder_no -= 1
                    folder.save()
            else:
                for item in items:
                    item.sequence_no -= 1
                    item.save()
        # Clone entities
        else:
            for item in items:
                item.sequence_no += 1
                item.save()
