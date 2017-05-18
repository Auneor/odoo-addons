# -*- coding: utf-8 -*-

import urlparse
import werkzeug.urls

from openerp import models, fields, api
from openerp.osv import osv

from openerp import tools
from openerp.tools.translate import _

# Overrides mass mailing Contact for this module purpose
class contact(models.Model):
	_name = "mail.mass_mailing.contact"
	_inherit = "mail.mass_mailing.contact"
	
	unsubscription_date = fields.Date(string="Unsubscription date")
	unsubscribed_by_odoo_user = fields.Many2one("res.users", string="Unsubscribed by this Odoo user")	

	_sql_constraints = [
		('email_list_unique',
		'unique (email, list_id)',
		_('Subscriber already registered for this mailing list.')
		)]
	
	@api.onchange("opt_out")
	def on_change_opt_out(self):
		if self.opt_out:
			self.unsubscription_date = fields.Datetime.now()
			self.unsubscribed_by_odoo_user = self.env.user
		else:
			self.unsubscription_date = None
			self.unsubscribed_by_odoo_user = None
			



class MailMail(osv.Model):
	"""Add the mass mailing campaign data to mail"""
	_name = 'mail.mail'
	_inherit = ['mail.mail']

	def _get_unsubscribe_url(self, cr, uid, mail, email_to, msg=None, context=None):
		if 'mass_mailing_test' in context:
			base_url = self.pool.get('ir.config_parameter').get_param(cr, uid, 'web.base.url')
		else:
			base_url = ""
		url = urlparse.urljoin(
			base_url, 'mail/mailing/%(mailing_id)s/unsubscribe?%(params)s' % {
				'mailing_id': mail.mailing_id.id,
				'params': werkzeug.url_encode({'db': cr.dbname, 'res_id': mail.res_id, 'email': email_to})
			}
		)
		return '%s' % url

	def _get_html_version_url(self, cr, uid, mail, email_to, context=None):
		if 'mass_mailing_test' in context:
			base_url = self.pool.get('ir.config_parameter').get_param(cr, uid, 'web.base.url')
		else:
			base_url = ""
		url = urlparse.urljoin(base_url, 'newsletter/html_version_%s' % mail.mailing_id.id)
		return '%s' % url

	def send_get_email_dict(self, cr, uid, mail, partner=None, context=None):	
		email_to = self.send_get_mail_to(cr, uid, mail, partner=partner, context=context)
		body = self.send_get_mail_body(cr, uid, mail, partner=partner, context=context)
		
		if mail.mailing_id and body and email_to:
			emails = tools.email_split(email_to[0])
			has_email_to = emails and emails[0] or False
			unsubscribe_url = self._get_unsubscribe_url(cr, uid, mail, has_email_to, context=context)
			if unsubscribe_url:
				body = body.replace('__UNSUBSCRIBE_URL__', unsubscribe_url)
			html_version_url = self._get_html_version_url(cr, uid, mail, has_email_to, context=context)
			body = body.replace('__HTML_VERSION_URL__', html_version_url)
			
		body_alternative = tools.html2plaintext(body)
		
		res = {
			'body': body,
			'body_alternative': body_alternative,
			'subject': self.send_get_mail_subject(cr, uid, mail, partner=partner, context=context),
			'email_to': email_to,
		}
		
		return res



class TestMassMailing(osv.TransientModel):
	_name = 'mail.mass_mailing.test'
	_description = 'Sample Mail Wizard'

	email_to = fields.Char('Recipients', required=True,help='Comma-separated list of email addresses.',default=lambda self: self.pool['mail.message']._get_default_from(self.env.cr, self.env.user.id, context=self.env.context))
	mass_mailing_id = fields.Many2one('mail.mass_mailing', 'Mailing', required=True, ondelete='cascade')

	def send_mail_test(self, cr, uid, ids, context=None):
		#Add a 'mass_mailing_test' flag in the context to be able to build correct HTML_VERSION/UNSUBSCRIBE URLs in test mode
		context['mass_mailing_test'] = True
		
		Mail = self.pool['mail.mail']
		for wizard in self.browse(cr, uid, ids, context=context):
			mailing = wizard.mass_mailing_id
			test_emails = tools.email_split(wizard.email_to)
			mail_ids = []
			for test_mail in test_emails:
				mail_values = {
					'email_from': mailing.email_from,
					'reply_to': mailing.reply_to,
					'email_to': test_mail,
					'subject': mailing.name,
					'body_html': '',
					'notification': True,
					'mailing_id': mailing.id,
					'attachment_ids': [(4, attachment.id) for attachment in mailing.attachment_ids],
				}
				mail_mail_obj = Mail.browse(cr, uid, Mail.create(cr, uid, mail_values, context=context), context=context)
				unsubscribe_url = Mail._get_unsubscribe_url(cr, uid, mail_mail_obj, test_mail, context=context)
				html_version_url = Mail._get_html_version_url(cr, uid, mail_mail_obj, test_mail, context=context)
				body = mailing.body_html.replace('__UNSUBSCRIBE_URL__', unsubscribe_url)
				body = mailing.body_html.replace('__HTML_VERSION_URL__', html_version_url)
				Mail.write(cr, uid, mail_mail_obj.id, {'body_html': mailing.body_html}, context=context)
				mail_ids.append(mail_mail_obj.id)
			Mail.send(cr, uid, mail_ids, context=context)
			self.pool['mail.mass_mailing'].write(cr, uid, [mailing.id], {'state': 'test'}, context=context)
		return True
	
#class MassMailing(osv.Model):
	#_name = "mail.mass_mailing"
	#_inherit = "mail.mass_mailing"



	#def _get_mailing_model(self, cr, uid, context=None):
	#	res = super(MassMailing, self)._get_mailing_model(cr, uid, context)
	#	res.append(('mail.tracking.email', _('Email Tracking')))
	#	print res
	#	return res	
	
	# indirections for inheritance
	#_mailing_model = lambda self, *args, **kwargs: self._get_mailing_model_groupeurd(*args, **kwargs)

	#_columns = {
		# recipients
	#	'mailing_model': fields.selection(_mailing_model, string='Recipients Model', required=True)
	#}

	#def action_edit_html(self, cr, uid, ids, context=None):
	#	if not len(ids) == 1:
	#		raise ValueError('One and only one ID allowed for this action')
	#	mail = self.browse(cr, uid, ids[0], context=context)
		
	#	if mail.mailing_model == 'mail.mass_mailing.contact' :
	#		template_model = 'mail.tracking.email'
	#	else:
	#		template_model = mail.mailing_model
		
		
		#url = '/website_mail/email_designer?model=mail.mass_mailing&res_id=%d&template_model=%s&return_action=%d&enable_editor=1' % (ids[0], mail.mailing_model, context['params']['action'])
	#	url = '/website_mail/email_designer?model=mail.mass_mailing&res_id=%d&template_model=%s&return_action=%d&enable_editor=1' % (ids[0], template_model, context['params']['action'])
	#	return {
	#		'name': _('Open with Visual Editor'),
	#		'type': 'ir.actions.act_url',
	#		'url': url,
	#		'target': 'self',
	#	}