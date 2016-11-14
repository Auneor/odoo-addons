# -*- coding: utf-8 -*-
{
    'name': "groupeurd_calendar",

    'summary': """
        Adaptation du module "smile_event_event_calendar" pour les besoins spécifiques du Groupe URD.""",

    'description': """
		- nouveau champ "équipe" dans évènement public pour le faire apparaître dans les calendriers de tous ses organisateurs/formateurs
		- calendrier unique par salarié avec évènements personnels, évènements communs, et à terme évènements à inscription publique
		=> synchroniser les évènements publics dans le calendrier personnel du responsable et des organisateurs/formateurs de l'évènement (ces évènements publics ne seront pas modifiables depuis les agendas personnels)
		- visibilité des calendriers de tous les autres salariés
		- accès à des vues personnalisées : planning de tous les salariés par semaine, planning de tous les salariés par mois
		- synchro bi-directionnelle avec Thunderbird
		- [optionnel] partage .ics des calendriers
    """,

    'author': "Groupe URD",
    'website': "http://www.urd.org",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/10.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Events',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['smile_event_event_calendar'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo.xml',
    ],
}