# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class MisAuhPartner1(models.Model):
    _inherit = 'hr.employee'

    joining_date = fields.Date('Joining Date', groups="hr.group_hr_user", tracking=True)
    passport_issued_date = fields.Date('Passport Issued Date', groups="hr.group_hr_user", tracking=True)
    passport_expiry_date = fields.Date('Passport Expiry Date', groups="hr.group_hr_user", tracking=True)
    visa_issued_date = fields.Date('Visa Issued Date', groups="hr.group_hr_user", tracking=True)

    work_issued_date = fields.Date('Work Permit Issued Date', groups="hr.group_hr_user", tracking=True)
    work_expiry_date = fields.Date('Work Permit Expiry Date', groups="hr.group_hr_user", tracking=True)
    insurance_no = fields.Char('Insurance No', groups="hr.group_hr_user", tracking=True)
    insurance_issued_date = fields.Date('Insurance Issued Date', groups="hr.group_hr_user", tracking=True)
    insurance_expiry_date = fields.Date('Insurance Expiry Date', groups="hr.group_hr_user", tracking=True)
    custom_back = fields.Binary('Custome Background')


