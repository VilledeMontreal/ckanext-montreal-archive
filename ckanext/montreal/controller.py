from ckan.lib import base
import ckan.plugins.toolkit as toolkit
import ckan.logic as logic
import ckan.lib.navl.dictization_functions as dictization_functions
import ckan.plugins as p
import ckan.lib.captcha as captcha
import ckan.lib.helpers as h
from ckan.common import _, request, c
from pylons import config
import logging
import emailer

log = logging.getLogger(__name__)
render = base.render
BaseController = base.BaseController
render = base.render
abort = base.abort
unflatten = dictization_functions.unflatten


class StaticController(BaseController):
    def newsletter(self):
        return toolkit.render('newsletter.html')


class ContactController(BaseController):
        @staticmethod
        def _submit():
            try:
                data_dict = logic.clean_dict(
                    unflatten(logic.tuplize_dict(logic.parse_params(request.params))))
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

                # TODO e-mail file attachment, param:to fallback
                content = """Sent by:{newline}
                             Name: {name}{newline}
                             Email: {email}{newline}{newline}
                             Message:{newline}{content}""".format(
                             name=data_dict['name'],
                             email=data_dict['email'],
                             content=data_dict['content'],
                             newline='</br>')
                to = config.get('ckanext.montreal.contact_mail_to')
                subject = "E-mail from contact form"
                try:
                    emailer.send_email(content=content, to=to, subject=subject)
                except Exception as e:
                    log.error(e)
                    h.flash_error(
                        _(u'Sorry, there was an error sending the email. Please try again later'))
                else:
                    data_dict['success'] = True

            return data_dict, errors, error_summary

        def contact_form(self):
            data = {}
            errors = {}
            error_summary = {}

            # Submit the data
            if 'save' in request.params:
                data, errors, error_summary = self._submit()
            else:
                # Try and use logged in user values for default values
                try:
                    data['name'] = c.userobj.fullname or c.userobj.name
                    data['email'] = c.userobj.email
                except AttributeError:
                    data['name'] = data['email'] = None
            if data.get('success', False):
                return p.toolkit.render('contact/success.html')
            else:
                vars = {'data': data, 'errors': errors, 'error_summary': error_summary}
                return p.toolkit.render('contact/form.html', extra_vars=vars)
