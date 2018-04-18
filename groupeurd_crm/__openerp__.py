# -*- coding: utf-8 -*-
{
    'name': "groupeurd_crm",

    'summary': """
        Paramétrage d'Odoo pour correspondre aux besoins CRM du Groupe URD.""",

    'description': """
		- Ajout de champs personnalisés
		- Personnalisation des listes d’affichage (tri, colonnes, filtres)
		- Personnalisation des écrans d’affichage des entités : position des champs, organisation par groupe des champs, champs obligatoires/facultatifs
		- Masquer les éléments "Clients" et "Pistes" du sous-menu "Ventes" jusqu'à ce que le besoin de suivi de pistes soit remonté
		- Publier en webpage des listes de nom/id_externe pour les Listes de diffusion, les Catégories de contact, et les Civilités de contact
		- Ajouter une liste de 0 à 5 "Pays d'expertise"
		- Ajouter un lien direct vers profil LinkedIn pour pâlier défaut plugin existant
		- Rendre le champ "Relation interne principale" accessible comme champ de recherche avancé, et le remplir par défaut par le créateur du contact
		- Renommer "Nom" en "Nom de famille" pour distinguer le nom de famille du "Nom" qui est l'association Prénom + Nom de famille
		 
		Contacts, ajout des champs:
		Compte de réseau social (Skype, Twitter, LinkedIn, Facebook), Langue principale, langues secondaires, Publications (liste d’URL).
		
		Organisation, ajout des champs:
		budget annuel, langue principale, langues secondaires, état d’adoption de Sigmah (Prise d’information, Souhait d’adoption, Adoption démarrée, Utilisation partielle, Utilisation complète, Non), zone de commentaires.
		
		Installation:
		Pour avoir un Mail de rappel pour compléter organisation après opportunité Sigmah gagnée, créer une "Action automatisée" en utilisant le domaine
			suivant comme filtre: 	[('categ_ids.name', '=','Adoption Sigmah'),('stage_id.name','=','Gagné')]

    """,

    'author': "Groupe URD",
    'website': "http://www.urd.org",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base', 'calendar_ics', 'groupeurd_newsletter', 'crm', 'partner_social_fields'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'templates.xml', 
		'actions-menus.xml',
		'views.xml',
        'data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}