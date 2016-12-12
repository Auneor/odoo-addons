# -*- coding: utf-8 -*-

from openerp import models, fields, api

#Debuggger package
import pdb
##		APPELER "pdb.set_trace()" pour faire un point de débuggage qu'on peut piloter ensuite depuis la console

#
# "event.event" est l'objet pour les évènements publics
#
class Event(models.Model):
	_name = "event.event"
	_inherit = "event.event"
	
	#le champ "team_ids" est conçu pour n'etre modifiable que depuis l'interface sur un event.event
	#   => il sert d'interface pour modifier le calendar_event.partner_ids qui lui stocke la valeur de référence sur cette information
	team_ids = fields.Many2many("res.partner", string="Event team members")

	
	# le décorateur "@api.model" indique que le "self" est alors une classe "event.event" générique
	@api.model
	def create(self, vals):
		#Ajouter le responsable (user_id) à l'équipe pour que l'évènement soit visible dans son calendrier
		team_ids_vals = vals['team_ids'][0][2] 
		team_ids_vals.append(self.env['res.users'].search([('id','=',vals['user_id'])]).partner_id.id)
		vals['team_ids'] = [(6,False,team_ids_vals)]
		
		event = super(Event, self).create(vals)
			
		return event

	# le décorateur "@api.multi" indique que le "self" dans la fonction est tableau d'objets "event.event"
	@api.multi
	def write(self, vals):
		# Ajouter le responsable (user_id) à l'équipe s'il a été modifié
		if vals.get('user_id'):
			team_ids_vals = []
			if vals.get('team_ids'):
				team_ids_vals = vals['team_ids'][0][2]
			else:				
				event = self
				for team_member_id in event.team_ids:
					team_ids_vals.append(team_member_id.id) 
			team_ids_vals.append(self.env['res.users'].search([('id','=',vals['user_id'])]).partner_id.id)
			vals['team_ids'] = [(6,False,team_ids_vals)]		
		
		res = super(Event, self).write(vals)
		context = dict(self._context or {})
		if context.get("from_eventevent_interface"):
			for event in self:
				for calendar_event in self.env['calendar.event'].search([('event_event_id','=',event.id)]):
					calendar_event.partner_ids = event.team_ids
					if vals.get('user_id'):
						calendar_event.user_id = event.user_id
		return res
	

#
# "calendar.event" est l'objet pour les évènements affichés dans les calendriers des utilisateurs
#
class CalendarEvent(models.Model):
	_inherit = 'calendar.event'

	@api.model
	def create(self, vals):
		calendar_event = super(CalendarEvent, self).create(vals)
		if calendar_event.event_event_id:
			calendar_event.partner_ids = calendar_event.event_event_id.team_ids
			calendar_event.partner_ids |= calendar_event.event_event_id.user_id.partner_id
		return calendar_event

	@api.multi
	def write(self, vals):
		res = super(CalendarEvent, self).write(vals)
		
		# Après la modification, si la modif n'est pas faite depuis l'event.event,
		# on met à jour la team member listes de l'event.event
		context = dict(self._context or {})
		if context.get("from_eventevent_interface") != True :
			for calendar_event in self:
				if calendar_event.event_event_id:
					calendar_event.event_event_id.team_ids = calendar_event.partner_ids
		
		return res


		
	
#Overrides calendar_ics "res_partner" override to have our custom URL
class res_partner(models.Model):
    _inherit = "res.partner"
    @api.one
    def create_ics_url(self):
        self.ics_url_field = '%s/calendar-ics/%s/public.ics' % (self.env['ir.config_parameter'].sudo().get_param('web.base.url'), self.id)

		
