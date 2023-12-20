
from odoo.http import Controller, request, route
import base64

from odoo import http
class HrEmployee(Controller):

    @route('/expense', type='http', auth='user', website = True)
    def get_hr_expense(self, **post):
        employee = request.env.user.employee_id
        dashboard_status =  request.env['hr.expense'].sudo().get_expense_portal_state(employee.id)
        expense_list =  request.env['hr.expense'].sudo().search([('employee_id','=',employee.id)])
        expense_product_list =  request.env['product.product'].sudo().search([('can_be_expensed','=',True)])
        return request.render('tecfuge_hrms.portal_hr_expense_main',{'employee':employee,'dashboard_status':dashboard_status,'expense_list':expense_list,'expense_product_list':expense_product_list})

    @route('/expense/submit', type='http', auth='user',methods=['POST'],csrf=False, website=True)
    def get_hr_submit_of_expense(self, **post):

        document_file = post['message_main_attachment_id']
        if document_file.filename:
            document_attachment = request.env['ir.attachment'].sudo().create({
                'name': document_file.filename,
                'datas': base64.encodebytes(document_file.read()),
                'type': 'binary',
                'public': True
            })
        expense=request.env['hr.expense'].sudo().create({
            'employee_id':request.env.user.employee_id.id,
            'name': post['name'],
            'date': post['date'],
            'product_id': int(post['product_id']),
            'total_amount': int(post['total_amount']),
        })
        expense.attachment_ids = document_attachment
        return  request.redirect('/expense')