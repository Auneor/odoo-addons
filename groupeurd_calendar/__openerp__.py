# -*- coding: utf-8 -*-
{
    'name': "groupeurd_calendar",

    'summary': """
        Adaptation des modules "smile_event_event_calendar" & "calendar_ics" pour les besoins spécifiques du Groupe URD.""",

    'description': """
		- nouveau champ "équipe" dans évènement public pour le faire apparaître dans les calendriers de tous ses organisateurs/formateurs
		- calendrier unique par salarié avec évènements personnels, évènements communs, et évènements publics (synchroniser les évènements publics dans le calendrier personnel du responsable et des organisateurs/formateurs de l'évènement (ces évènements publics ne seront pas modifiables depuis les agendas personnels)
		- visibilité des calendriers de tous les autres salariés
		- accès à des vues personnalisées : planning de tous les salariés par semaine, planning de tous les salariés par mois
		- synchro bi-directionnelle avec Thunderbird
		- partage .ics des calendriers
		- masquer tout le sous-menu "Messagerie" et transformer le menu parent en "Agenda"
		- renommer l'agenda personnel appelé "Meetings Calendar" dans l'interface
		- descendre "évènement public" sous la case à cocher "toute la journée" dans la popup de modification d'un évènement de l'agenda personnel
		- ajouter l'accès à "Invitations & divers" des évènements personnels à tous les utilisateurs
		- retirer la possibilité de modifier tous les évènements par tout le monde, même quand ils ne sont pas invités à l'évènment
		- Masquer l'option "orateur" d'un contact d'une organisation
		
		
		INSTALLATION
		- Lors de l'installation, modifier le Filtre de domaine de la règle "Hide Private Meetings" à la valeur suivante ['|',('user_id','=',user.id),'|',('show_as','=','busy'),('show_as','=','free')] (cela permet d'afficher les évènements (calendar.event) qui sont de type disponibles)
		- Attention, le partage ics de calendrier et la synchro Thunderbird ne fonctionneront que sur une instance Odoo mono-base
		- Retirer les droits de création/modification/suppression à l'enregistrement de sécurité "All Calendar Event for employees" (calendar.calendar_event_rule_employee)
		- Ajouter le groupe utilisateur "Ressources humaines/Employé" à l'enregistrement de sécurité "Own events" (calendar.calendar_event_rule_my)
    """,

    'author': "Groupe URD",
    'website': "http://www.urd.org",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/10.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Events',
    'version': '0.3',

    # any module necessary for this one to work correctly
    'depends': ['smile_event_event_calendar', 'calendar_ics', 'mail'],

    # always loaded
    'data': [
        'views.xml', 
		'actions-menus.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo.xml',
    ],
}