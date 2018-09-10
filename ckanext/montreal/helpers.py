from ckan.plugins import toolkit


def get_groups():
    # Helper used on the homepage for showing groups

    data_dict = {
        'all_fields': True
    }
    groups = toolkit.get_action('group_list')({}, data_dict)

    return groups
