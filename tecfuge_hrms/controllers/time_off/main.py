
from odoo.http import Controller, request, route
import base64


class HrEmployee(Controller):

    @route('/timeoff', type='http', auth='user',website = True)
    def get_hr_time_off(self, **post):
        employee = request.env.user.employee_id
        time_off = request.env['hr.leave'].sudo().search([('employee_id','=',employee.id)])
        time_off_type = request.env['hr.leave.type'].sudo().search(['|',('has_valid_allocation','=',True),('requires_allocation','=','no')])
        time_off_summary = request.env['hr.leave.type'].sudo().get_days_all_portal(employee.id)
        return request.render('tecfuge_hrms.portal_hr_leave_main',{'employee':employee,'time_off':time_off,'time_off_type':time_off_type,'time_off_summary':time_off_summary})

    @route('/timeoff/submit', type='http', auth='user',methods=["POST"],csrf=False,website = True)
    def get_submit_time_off(self, **post):
        time_off = request.env['hr.leave'].sudo().create({
            'employee_id': request.env.user.employee_id.id,
            'holiday_status_id': int(post['holiday_status_id']),
            'date_from': post['date_from'],
            'request_date_from': post['date_from'],
            'request_date_to': post['date_to'],
            'date_to':post['date_to'],
            'name':post['name']
        })
        document_file = post['attachment_id']
        if document_file.filename:
            document_attachment = request.env['ir.attachment'].sudo().create({
                'name': document_file.filename,
                'datas': base64.encodebytes(document_file.read()),
                'type': 'binary',
                'public': True
            })

        time_off.message_post(body="Support Documents", attachments=document_attachment)


        time_off.attachment_id = [document_attachment.id]

        return request.redirect('/timeoff')