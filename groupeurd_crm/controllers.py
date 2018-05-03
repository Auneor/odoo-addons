# -*- coding: utf-8 -*-
from openerp import http, SUPERUSER_ID
from openerp.http import request

from openerp.tools.translate import _

import logging
_logger = logging.getLogger(__name__)

class GroupeURD_CRM(http.Controller):
	
	#Example: /crm/list_mailing_lists?db=groupeurd-openacademy
	@http.route('/crm/list_mailing_lists', auth='public')
	def view_mailing_lists(self, db):
		http.request.session.db = db
		http.request.cr.execute("""
select mmml.name as mailing_list, imd.module || '.' || imd.name as external_id
from ir_model_data imd
inner join mail_mass_mailing_list mmml on mmml.id = imd.res_id
where imd.model = 'mail.mass_mailing.list'
order by mmml.name;	
		""")
		mailing_lists = http.request.cr.dictfetchall()
		output = ""
		for i, val in enumerate(mailing_lists):
			output = output + val['mailing_list'] + "\t" + val['external_id'] + "\n"
		return output
	
	#Example: /crm/list_partner_categories?db=groupeurd-openacademy
	@http.route('/crm/list_partner_categories', auth='public')
	def view_partner_categories(self, db):
		http.request.session.db = db
		http.request.cr.execute("""
select rpc.name as category, imd.module || '.' || imd.name as external_id
from ir_model_data imd
inner join res_partner_category rpc on rpc.id = imd.res_id
where imd.model = 'res.partner.category'
order by rpc.name;	
		""")
		partner_categories = http.request.cr.dictfetchall()
		output = ""
		for i, val in enumerate(partner_categories):
			output = output + val['category'] + "\t" + val['external_id'] + "\n"
		return output
		
	
	#Example: /crm/list_partner_titles?db=groupeurd-openacademy
	@http.route('/crm/list_partner_titles', auth='public')
	def view_partner_titles(self, db):
		http.request.session.db = db
		http.request.cr.execute("""
select rpt.name as title, imd.module || '.' || imd.name as external_id
from ir_model_data imd
inner join res_partner_title rpt on rpt.id = imd.res_id
where imd.model = 'res.partner.title'
order by rpt.name;	
		""")
		partner_titles = http.request.cr.dictfetchall()
		output = ""
		for i, val in enumerate(partner_titles):
			output = output + val['title'] + "\t" + val['external_id'] + "\n"
		return output
		
	
	#Example: /crm/list_languagelist?db=groupeurd-openacademy
	@http.route('/crm/list_languagelist', auth='public')
	def view_languagelist(self, db):
		http.request.session.db = db
		http.request.cr.execute("""
select gcl.name as language, imd.module || '.' || imd.name as external_id
from ir_model_data imd
inner join groupeurd_crm_languagelist gcl on gcl.id = imd.res_id
where imd.model = 'groupeurd_crm.languagelist'
order by gcl.name;
		""")
		languagelist = http.request.cr.dictfetchall()
		output = ""
		for i, val in enumerate(languagelist):
			output = output + val['language'] + "\t" + val['external_id'] + "\n"
		return output
