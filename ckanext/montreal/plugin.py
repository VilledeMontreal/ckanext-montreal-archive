import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckanext.montreal import helpers


class MontrealPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'montreal')

    # ITemplateHelpers

    def get_helpers(self):
        return {
            'montreal_get_groups': helpers.get_groups,
            'get_recently_updated_datasets':
                helpers.get_recently_updated_datasets,

        }
