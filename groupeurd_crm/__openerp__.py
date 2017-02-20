# -*- coding: utf-8 -*-
{
    'name': "groupeurd_crm",

    'summary': """
        Paramétrage d'Odoo pour correspondre aux besoins CRM du Groupe URD.""",

    'description': """
		- Ajout de champs personnalisés
			- Personnalisation des listes d’affichage (tri, colonnes, filtres)
		 - Personnalisation des écrans d’affichage des entités : position des champs, organisation par groupe des champs, champs obligatoires/facultatifs
		 - Masquer le sous-menu "Ventes" jusqu'à ce que le besoin de suivi de pistes et opportunités soit remonté
		 
		 
		Organisation
		Nom, adresse (prévoir 3 lignes), Code postal, Pays, Téléphone, Télécopie, site web, budget annuel, langue principale, langue(s) secondaire(s), état d’adoption de Sigmah (Prise d’information, Souhait d’adoption, Adoption démarrée, Utilisation partielle, Utilisation complète, Non), zone de commentaires.

		Contacts
		Civilité, Nom, prénom, fonction, type de fonction (liste de valeurs paramétrables) adresse (prévoir 3 lignes), code postal, pays, téléphone bureau, téléphone mobile, adresse mail, compte de réseau social (Skype, Twitter, LinkedIn, Facebook), Langue principale, langue(s) secondaires(s), niveau de contact (cercle de proximité de la relation), niveau universitaire, Centres d’intérêt (Liste de valeur, multisélection), compétences (Liste de valeur, multisélection) et nombre d’années dans la compétence sélectionnée, Publications (liste d’URL), zone de commentaires.
    """,

    'author': "Groupe URD",
    'website': "http://www.urd.org",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'calendar_ics', 'groupeurd_newsletter'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml', 
		'actions-menus.xml',
		'views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}