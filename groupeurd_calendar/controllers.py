# -*- coding: utf-8 -*-
from openerp import http
from openerp.http import request

class res_partner_icalendar(http.Controller):
    @http.route(['/calendar-ics/<partner_id>/public.ics'], auth="public")
    def icalendar_public(self, partner_id, **post):
        #pdb.set_trace()
        
        partner = http.request.env['res.partner'].sudo().search([('id','=',partner_id)])
        if partner:
            document = partner.sudo().get_ics_calendar(type='public')
            return request.make_response(
                document,
                headers=[
                    ('Content-Disposition', 'attachment; filename="public.ics"'),
                    ('Content-Type', 'text/calendar'),
                    ('Content-Length', len(document)),
                ]
            )
        else:
            raise Warning("Public failed")
            pass # Some error page