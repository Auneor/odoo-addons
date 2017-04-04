# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.osv import osv

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
		return ""


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