# -*- coding: utf-8 -*-
from openerp import http, SUPERUSER_ID
from openerp.http import request

from openerp.addons.mass_mailing.controllers.main import MassMailController
from openerp.tools.translate import _

class GroupeURD_Newsletter(http.Controller):
	@http.route('/newsletter/html_version_<massmailing_id>', auth='public')
	def view_newsletter_html_version(self, massmailing_id):
		mass_mailing = http.request.env['mail.mass_mailing'].search([('id','=',massmailing_id)])
		return mass_mailing.body_html

##class GroupeURD_MassMailController(MassMailController):
##
##	#Add nicer message on unsubscribe
##	@http.route(['/mail/mailing/<int:mailing_id>/unsubscribe'], type='http', auth='none')
##	def mailing(self, mailing_id, email=None, res_id=None, **post):
##		sup_Controller = super(MassMailController, self)
##		basic_result_message = sup_Controller.mailing(mailing_id, email, res_id, **post)
##		
##		# part of the method added to have a nicer message
##		res_contact = http.request.env['mail.mass_mailing.contact'].search([('id','=',res_id)])
##		html_result_message = '<div style="text-align:center">'
##		if basic_result_message == 'OK':
##			html_result_message += _("The following email address has been successfully unsubscribed from the list")
##			html_result_message += ' "%s" : ' % res_contact.list_id.name
##			html_result_message += email
##		else:
##			html_result_message += _("Unable to unsubscribe the following email address from the list")
##			html_result_message += ' "%s" : ' % res_contact.list_id.name
##			html_result_message += email
##		html_result_message += '</div>'
##		return html_result_message



		
