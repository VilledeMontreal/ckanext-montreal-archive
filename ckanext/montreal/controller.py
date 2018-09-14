from ckan.lib import base
import ckan.plugins.toolkit as toolkit

render = base.render
BaseController = base.BaseController


class StaticController(BaseController):
    def newsletter(self):
        return toolkit.render('newsletter.html')
