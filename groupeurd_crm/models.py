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
	

# Surcharge l'objet "Contact" pour ajouter les liens vers les objets "Abonné" et "Liste de diffusion"
class partner(models.Model):
	_name = "res.partner"
	_inherit = "res.partner"
	
	list_ids = fields.Many2many("mail.mass_mailing.list", string="Listes de diffusion")
	contact_ids = fields.One2many("mail.mass_mailing.contact", "partner_id", string="Abonnements")
	secondary_language1 = fields.Selection(tools.scan_languages(), string="Langue secondaire 1")	
	secondary_language2 = fields.Selection(tools.scan_languages(), string="Langue secondaire 2")	
	secondary_language3 = fields.Selection(tools.scan_languages(), string="Langue secondaire 3")	
	
	
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
	
	
		
	
	# A FAIRE
	# A la création de contact, mettre à jour contact_ids et list_ids en fonction des abonnements existants pour cette adresse email
	# A la modification de contact, mettre à jour contact_ids et list_ids en fonction des abonnements existants pour cette adresse email
	
