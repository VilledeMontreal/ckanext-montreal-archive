from ckan.plugins import toolkit

import logging
from datetime import datetime
from pprint import pprint

log = logging.getLogger()


def get_groups():
    # Helper used on the homepage for showing groups

    data_dict = {
        'all_fields': True
    }
    groups = toolkit.get_action('group_list')({}, data_dict)

    return groups


def get_recently_updated_datasets(limit=5):
    '''
     Returns recent created or updated datasets.
    :param limit: Limit of the datasets to be returned. Default is 5.
    :type limit: integer
    :returns: a list of recently created or updated datasets
    :rtype: list
    '''
    try:
        pkg_search_results = toolkit.get_action('package_search')(data_dict={
            'sort': 'metadata_modified desc',
            'rows': limit,
        })['results']
    except:
        return []
    else:
        pkgs = []
        for pkg in pkg_search_results:
            package = toolkit.get_action('package_show')(
                data_dict={'id': pkg['id']})
            modified = datetime.strptime(
                package['metadata_modified'].split('T')[0], '%Y-%m-%d')
            package['days_ago_modified'] = ((datetime.now() - modified).days)
            pkgs.append(package)
        pprint(pkgs)
        return pkgs
