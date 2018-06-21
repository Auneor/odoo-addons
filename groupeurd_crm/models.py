# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.osv import osv
from openerp import tools

from openerp.tools.translate import _

# Surcharge l'objet "Abonné" pour ajouter un lien vers l'objet "Contact"
class contact(models.Model):
	_name = "mail.mass_mailing.contact"
	_inherit = "mail.mass_mailing.contact"
	
	partner_id = fields.Many2one("res.partner", string="Contact")	
	
	@api.model
	def create(self, vals):
		new_id = super(contact, self).create(vals)
		partner = self.env['res.partner'].search([('email','=',new_id.email)])
		if partner:
			new_id.partner_id = partner[0].id # "new_id.partner_id" plutôt que "self.partner_id" car le self est vide dans un create
			if new_id.list_id not in new_id.partner_id.list_ids:
				new_id.partner_id.list_ids |= new_id.list_id
		return new_id

class languagelist(models.Model):
	_name = "groupeurd_crm.languagelist"
	
	locale = fields.Char(required = True, string="Locale")
	name = fields.Char(required = True, string="Nom de la langue")

# Surcharge l'objet "Contact" pour ajouter les liens vers les objets "Abonné" et "Liste de diffusion"
class partner(models.Model):
	_name = "res.partner"
	_inherit = "res.partner"
	
	list_ids = fields.Many2many("mail.mass_mailing.list", string="Listes de diffusion")
	contact_ids = fields.One2many("mail.mass_mailing.contact", "partner_id", string="Abonnements")
	secondary_languages = fields.Many2many("groupeurd_crm.languagelist", string="Langues secondaires")
	country_experiences = fields.Many2many("res.country", string="Pays d'expertise")
	linkedin = fields.Char(string="LinkedIn")
	moodle_username = fields.Char(string="Moodle username")
	
	yearly_budget = fields.Integer(string="Budget annuel de l'organisation (M€)")
	sigmah_adoption_status = fields.Selection([('no',"Non"),('engaged',"Adoption engagée"),('partial',"Utilisation partielle"),('complete',"Utilisation complète")], default='no', string="Adoption de Sigmah", required=True)
	sigmah_package = fields.Selection([('basic',"socle"),('full',"complet")], string="Forfait de services")
	sigmah_use_start = fields.Date(string="Début d'utilisation")
	sigmah_autonomous_hosting = fields.Boolean(default=False, string="Hébergement autonome")
	sigmah_users_count = fields.Integer(string="Nombre d'utilisateurs de Sigmah")
	
	#Si des listes de diffusion sont ajoutées à la création du "Contact", ajouter les abonnements en conséquence
	@api.model
	def create(self, vals):				
		#On fait la création d'abord pour pouvoir associer les abonnements ensuite
		res = super(partner, self).create(vals)
		
		#Ajout de listes: pour toutes les listes en valeur, créer l'abonnement
		subscribe_contact_vals_array = []
		if vals.get('list_ids'):
			for list_id in vals['list_ids'][0][2]:
				list = self.env['mail.mass_mailing.list'].browse(list_id)
				subscribe_contact_vals_array.append({'email': vals.get('email'), 'list_id':list_id})
		
		
		#Appliquer les ajout de listes
		for contact_vals in subscribe_contact_vals_array: 
			self.env['mail.mass_mailing.contact'].create(contact_vals)	
			
		return res
	
		
	
	#Si des listes de diffusion sont ajoutées/supprimées pour le "Contact", modifier les abonnements en conséquence
	@api.multi
	def write(self, vals):		
		#Ajout de listes: pour toutes les listes en valeur, si une liste n'est pas dans les listes existantes, créer l'abonnement
		subscribe_contact_vals_array = []
		if vals.get('list_ids'):
			for list_id in vals['list_ids'][0][2]:
				list = self.env['mail.mass_mailing.list'].browse(list_id)
				for partner_element in self:
					if list not in partner_element.list_ids:
						subscribe_contact_vals_array.append({'email': partner_element.email, 'list_id':list_id})
		
			
		#Suppression de listes: pour toutes les listes existantes, si l'une d'elle n'est plus dans les listes passées en valeur, supprimer l'abonnement
		unsubscribe_list_ids = []
		for partner_element in self:
			for list in partner_element.list_ids:
				if vals.get('list_ids'):
					if list.id not in vals['list_ids'][0][2]:
						unsubscribe_list_ids.append(list.id)
		
		#On fait l'écriture avant les ajout de listes pour éviter les boucles
		res = super(partner, self).write(vals)
		
		#Appliquer les ajout de listes
		for contact_vals in subscribe_contact_vals_array: 
			self.env['mail.mass_mailing.contact'].create(contact_vals)
			
		#Appliquer les désincriptions
		for unsubscribe_list_id in unsubscribe_list_ids: 
			contact_array = self.env['mail.mass_mailing.contact'].search([('list_id','=',unsubscribe_list_id)])
			for contact in contact_array:
				contact.opt_out = True
				contact.unsubscription_date = fields.Datetime.now()
				contact.unsubscribed_by_odoo_user = self.env.user
		return res
	
	#Si des listes de diffusion ont été ajoutées pour le "Contact", supprimer les abonnements en conséquence lors de la suppression du contact
	@api.multi
	def unlink(self):
		#Appliquer les désincriptions
		for partner_element in self:
			contact_array = self.env['mail.mass_mailing.contact'].search([('email','=',partner_element.email)])
			for contact in contact_array:
				contact.opt_out = True
				contact.unsubscription_date = fields.Datetime.now()
				contact.unsubscribed_by_odoo_user = self.env.user				
		
		#On fait la suppression après les désabonnements pour avoir l'objet partner toujours présent
		res = super(partner, self).unlink()
		
		return res
		
	
	def goto_linkedin(self, cr, uid, ids, context=None):
		partner_obj = self.pool.get('res.partner')
		partner = partner_obj.browse(cr, uid, ids, context=context)[0]
		if partner.linkedin:
			good_starting_urls = ['https://linkedin.com/', 'https://www.linkedin.com/', \
								  'http://linkedin.com/', 'http://www.linkedin.com/']
			non_protocol_starting_urls = ['linkedin.com/', 'www.linkedin.com/']
			
			if any(map(lambda x: partner.linkedin.startswith(x), good_starting_urls)):
				url = partner.linkedin
			elif any(map(lambda x: partner.linkedin.startswith(x), non_protocol_starting_urls)):
				url = 'https://' + partner.linkedin
			else:
				url = 'https://www.linkedin.com/' + partner.linkedin
			
			return {'type': 'ir.actions.act_url', 'url': url, 'target': 'new'}
		
	
	# A FAIRE
	# A la création de contact, mettre à jour contact_ids et list_ids en fonction des abonnements existants pour cette adresse email
	# A la modification de contact, mettre à jour contact_ids et list_ids en fonction des abonnements existants pour cette adresse email
	
