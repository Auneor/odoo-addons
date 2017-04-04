# -*- coding: utf-8 -*-
{
    'name': "groupeurd_newsletter",

    'summary': """
        Adaptation du module "mass_mailing" pour les besoins spécifiques du Groupe URD.""",

    'description': """
		- Renommer "contacts" en "abonnés" pour liste de diffusion
		- Renomer menu "Marketing" en "Listes de diffusion"
		- Unicité de l'abonné dans chaque liste
		- Droits d'utilisateur pour limiter accès à uniquement publipostages et listes de diffusion
		- Retirer droit de suppression d'abonné au profil Responsable Marketing
		- Retirer la gestion des nom des abonnés (dans la liste ou dans le formulaire)
		- Ajouter un champ "unsubscribed_by_odoo_user" qui sera manipulé pour les désincriptions par interface
		- Afficher champ create_uid pour savoir provenance des contacts
		- Ne garder que les modèles de courriel de newsletter dans Publipostages/Modèles de courriel
		- Retrait insertion automatique lien désinscription
		- Message de confirmation de désincription plus verbeux
		- Modèles de newsletter spécifiques
		
		En projet:
		- Ecraser les propriétés d'un publipostage par les propriétés standard d'un modèle de courriel au moment de la sélection de ce dernier.
    """,

    'author': "Groupe URD",
    'website': "http://www.urd.org",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Marketing',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base','mass_mailing','marketing','website_mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'actions-menus.xml',
        'views.xml',
		'newsletter-fr-template.xml',
		'newsletter-en-template.xml',
		'snippets.xml',
    ],
}