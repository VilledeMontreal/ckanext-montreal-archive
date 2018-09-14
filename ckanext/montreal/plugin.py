import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckanext.montreal import helpers


class MontrealPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IRoutes)

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

    # IRoutes

    def before_map(self, map):
        static_ctrl = 'ckanext.montreal.controller:StaticController'
        map.connect('newsletter', '/newsletter',
                    controller=static_ctrl, action='newsletter')
        return map

    def after_map(self, map):
        return map
