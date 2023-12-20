
from odoo.http import Controller, request, route
import base64


class HrEmployee(Controller):

    @route('/employee', type='http', auth='user',website = True)
    def get_hr_employee_details_dashboard(self, **post):
        employee = request.env.user.sudo().employee_id
        return request.render('tecfuge_hrms.portal_employee_details',{"employee":employee})

