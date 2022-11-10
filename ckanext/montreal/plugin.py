import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckanext.montreal import blueprint, helpers
from ckan.lib.plugins import DefaultTranslation


class MontrealPlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.ITranslation)

    def download(self, package_id, resource_id, file_name):
        # This enables download of JSON files.
        if response.content_type == 'application/json':
            # Use Response with content_disposition as attachement.
            response.content_disposition = 'attachment'
            # Use Application/octet-stream to trigger
            # Open/Download dialog in browser
            response.content_type = 'application/octet-stream'
            response.cache_control = 'no-cache';
        #Use ckan internal resource_download method
        return self.resource_download(package_id,resource_id,file_name)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('assets', 'montreal')

    # ITemplateHelpers

    def get_helpers(self):
        return {
            'montreal_get_groups': helpers.get_groups,
            'get_recently_updated_datasets':
                helpers.get_recently_updated_datasets,

        }

    # IBlueprint

    def get_blueprint(self):
        return blueprint.get_blueprints()
