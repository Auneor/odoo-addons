# -*- coding: utf-8 -*-
from openerp import http

# class GroupeurdCrm(http.Controller):
#     @http.route('/groupeurd_crm/groupeurd_crm/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/groupeurd_crm/groupeurd_crm/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('groupeurd_crm.listing', {
#             'root': '/groupeurd_crm/groupeurd_crm',
#             'objects': http.request.env['groupeurd_crm.groupeurd_crm'].search([]),
#         })

#     @http.route('/groupeurd_crm/groupeurd_crm/objects/<model("groupeurd_crm.groupeurd_crm"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('groupeurd_crm.object', {
#             'object': obj
#         })