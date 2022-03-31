from flask import Blueprint

from ckan.plugins import toolkit

montreal = Blueprint(u'montreal', __name__)

def newsletter():
    return toolkit.render('newsletter.html')

montreal.add_url_rule('/abonnement', view_func=newsletter)

def get_blueprints():
    return [montreal]