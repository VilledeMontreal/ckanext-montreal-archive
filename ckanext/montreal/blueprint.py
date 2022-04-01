import logging

from flask import Blueprint

from ckan.plugins import toolkit
from ckan import logic
from ckan.lib import base
from ckan.lib import captcha
from ckan.common import _, request, c, config
import ckan.lib.navl.dictization_functions as dictization_functions
import ckan.lib.helpers as h

from ckanext.montreal import emailer


montreal = Blueprint(u'montreal', __name__)


log = logging.getLogger(__name__)
unflatten = dictization_functions.unflatten


def newsletter():
    return toolkit.render('newsletter.html')


def contact_form():
    data = {}
    errors = {}
    error_summary = {}

    # Submit the data
    if 'save' in request.form:
        data, errors, error_summary = _submit()
    else:
        # Try and use logged in user values for default values
        try:
            data['name'] = c.userobj.fullname or c.userobj.name
            data['email'] = c.userobj.email
        except AttributeError:
            data['name'] = data['email'] = None
    if data.get('success', False):
        return toolkit.render('contact/success.html')
    else:
        vars = {'data': data,
                'errors': errors,
                'error_summary': error_summary}
        return toolkit.render('contact/form.html', extra_vars=vars)


def _submit():
    try:
        data_dict = logic.clean_dict(
            unflatten(logic.tuplize_dict(logic.parse_params(request.form))))
        if request.files['attachment']:
            file_ = request.files['attachment']
        else:
            file_ = None
        c.form = data_dict['name']
        captcha.check_recaptcha(request)
    except logic.NotAuthorized:
        base.abort(401, _('Not authorized to see this page'))
    except captcha.CaptchaError:
        error_msg = _(u'Bad Captcha. Please try again.')
        h.flash_error(error_msg)

    errors = {}
    error_summary = {}

    if data_dict["email"] == '':
        errors['email'] = [u'Missing Value']
        error_summary['email'] = u'Missing value'

    if data_dict["name"] == '':
        errors['name'] = [u'Missing Value']
        error_summary['name'] = u'Missing value'

    if data_dict["content"] == '':
        errors['content'] = [u'Missing Value']
        error_summary['content'] = u'Missing value'

    if len(errors) == 0:
        # TODO param:to fallback
        dataset = data_dict.get('dataset', None)
        to = config.get('ckanext.montreal.contact_mail_to')
        subject = u"E-mail from contact form: {category}".format(category=data_dict['category'])
        file = file_
        print("FAJLOT", file)
        content = """Sent by:{newline}
                        Name: {name}{newline}
                        Email: {email}{newline}""".format(
                        name=data_dict['name'],
                        email=data_dict['email'],
                        newline='<br>')

        if dataset:
            content += "Affected dataset/resource: {dataset}{newline}".format(dataset=dataset, newline='</br>')

        content += "{newline}Message:{newline}{content}".format(newline='</br>', content=data_dict['content'])

        try:
            emailer.send_email(content=content, to=to, subject=subject, file=file)
        except Exception as e:
            log.error(e)
            h.flash_error(
                _(u'Sorry, there was an error sending the email. Please try again later'))
        else:
            data_dict['success'] = True

    return data_dict, errors, error_summary


montreal.add_url_rule('/abonnement', view_func=newsletter)

montreal.add_url_rule('/nous-joindre',
                      view_func=contact_form,
                      methods=[u'GET', u'POST'])


def get_blueprints():
    return [montreal]
