# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.osv import osv

from openerp.tools.translate import _

# Surcharge l'objet "Abonné" pour ajouter un lien vers l'objet "Contact"
class contact(models.Model):
	_name = "mail.mass_mailing.contact"
	_inherit = "mail.mass_mailing.contact"
	
	partner_id = fields.Many2one("res.partner", string="Contact")	
	
	# A FAIRE
	# A la création d'un abonné, mettre à jour partner_id si un contact existe avec cette adresse email 
	# A FINIR !
	@api.model
	def create(self, vals):
		new_id = super(contact, self).create(vals)
		partner = self.env['res.partner'].search([('email','=',new_id.email)])
		if ( partner ):
			self.partner_id = partner.id
	

# Surcharge l'objet "Contact" pour ajouter les liens vers les objets "Abonné" et "Liste de diffusion"
class partner(models.Model):
	_name = "res.partner"
	_inherit = "res.partner"
	
	list_ids = fields.Many2many("mail.mass_mailing.list", string="Listes de diffusion")
	contact_ids = fields.One2many("mail.mass_mailing.contact", "partner_id", string="Abonnements")
	
	# A FAIRE
	# A la création de contact, mettre à jour contact_ids et list_ids en fonction des abonnements existants pour cette adresse email
	# A la modification de contact, mettre à jour contact_ids et list_ids en fonction des abonnements existants pour cette adresse email
	
