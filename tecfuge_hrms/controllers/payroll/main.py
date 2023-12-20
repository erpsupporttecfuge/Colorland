
from odoo.http import Controller, request, route
import base64
from odoo import http

class HrEmployee(Controller):




    @route('/payroll', type='http', auth='user',website = True)
    def get_hr_payroll(self, **post):
        employee = request.env.user.employee_id
        payslips = request.env['hr.payslip'].sudo().search([('employee_id','=',employee.id)])
        return request.render('tecfuge_hrms.portal_payroll_board',{'employee':employee,'payslips':payslips})

    @route('/payroll/form', type='http', auth='user', website=True)
    def get_hr_form_view_payroll(self, **post):

        employee = request.env.user.employee_id
        payslips = request.env['hr.payslip'].sudo().search([('employee_id', '=', employee.id),('id','=',post['id'])])
        return request.render('tecfuge_hrms.portal_payroll_form_view', {'employee': employee, 'payslips': payslips})

    @http.route('/payroll/download', csrf=False, type='http', auth="user", website=True)
    def print_payroll_in_portal(self, **kw):

        r = request.env['hr.payslip'].sudo().search([('id','=',int(kw['id']))])
        pdf, _ = request.env['ir.actions.report'].sudo()._render_qweb_pdf('hr_payroll.action_report_payslip', r.id)
        pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))]
        return request.make_response(pdf, headers=pdfhttpheaders)