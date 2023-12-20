
from odoo.http import Controller, request, route
import base64


class HrEmployee(Controller):

    @route('/letter_request', type='http', auth='user',website = True)
    def get_hr_helpdesk(self, **post):
        employee = request.env.user.employee_id
        teams = request.env['helpdesk.team'].sudo().search([])
        ticket_type = request.env['helpdesk.ticket.type'].sudo().search([])
        tickets = request.env['helpdesk.ticket'].sudo().search([('partner_id','=', request.env.user.partner_id.id)])
        return request.render('tecfuge_hrms.portal_helpdesk_tickets',{'employee':employee,'tickets':tickets,'teams':teams,'ticket_type':ticket_type})

    @route('/letter_request/submit', type='http',methods=['POST'], auth='user', csrf=False ,website = True)
    def get_hr_submit_helpdesk(self, **post):
        print("post",post)
        request.env['helpdesk.ticket'].sudo().create({
            'partner_id':request.env.user.partner_id.id,
            'name':post['name'],
            'team_id':int(post['team_id']),
            'ticket_type_id':int(post['type_id']),
            'description': post['description']

        })
        return request.redirect("/letter_request")