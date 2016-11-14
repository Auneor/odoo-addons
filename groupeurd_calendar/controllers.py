# -*- coding: utf-8 -*-
from openerp import http

# class GroupeurdCalendar(http.Controller):
#     @http.route('/groupeurd_calendar/groupeurd_calendar/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/groupeurd_calendar/groupeurd_calendar/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('groupeurd_calendar.listing', {
#             'root': '/groupeurd_calendar/groupeurd_calendar',
#             'objects': http.request.env['groupeurd_calendar.groupeurd_calendar'].search([]),
#         })

#     @http.route('/groupeurd_calendar/groupeurd_calendar/objects/<model("groupeurd_calendar.groupeurd_calendar"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('groupeurd_calendar.object', {
#             'object': obj
#         })