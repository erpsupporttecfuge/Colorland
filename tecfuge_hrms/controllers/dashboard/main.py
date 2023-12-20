
from odoo.http import Controller, request, route
import base64


class HrDashBoard(Controller):


    @route('/dashboard', type='http', auth='user',website = True)
    def get_hr_dashboard(self, **post):
        if request.env.user.has_group('base.group_portal'):
            employee = request.env.user.employee_id
            dashboard_status =  request.env['hr.expense'].sudo().get_expense_portal_state(employee.id)
            time_off_summary = request.env['hr.leave.type'].sudo().get_days_all_portal(employee.id)
            documents = request.env['res.document'].sudo().get_documents_table_in_portal(request.env.user.id)
            activities= request.env['mail.activity'].sudo().search([('user_id','=',request.env.user.id)])
            return request.render('tecfuge_hrms.portal_main_dashboard_hr',{'employee':employee,'dashboard_status':dashboard_status,'time_off_summary':time_off_summary,'documents':documents,'activities':activities})

        else:
            return request.redirect('/web')