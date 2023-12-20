from odoo import api, fields, models


from odoo import fields, models,api
from odoo.tools import format_date

class HrRecruitmentStage(models.Model):
    _inherit = 'hr.recruitment.stage'
    is_sent_offer = fields.Boolean(default=False)


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'
    is_visible = fields.Boolean(related='stage_id.is_sent_offer')
    def action_sent_test(self):
        pass
class HrLeavePublic(models.Model):
    _name = 'hr.leave.public'

    def get_dashboard_portal_calender_view(self, employee_id):
        employee_id = self.env['hr.employee'].sudo().search([('user_id', '=', employee_id)])
        data_json = []
        values = self.env['hr.leave'].sudo().search([('state', '=', 'validate'), ('employee_id', '=', employee_id.id)])
        for rec in values:
            record = {}
            if rec.name:
                record['title'] = rec.name + "[" + rec.holiday_status_id.name + "]"
            else:
                record['title'] = rec.holiday_status_id.name
            record['color'] = rec.holiday_status_id.color
            record['start'] = rec.date_from
            if rec.date_to:
                record['end'] = rec.date_to
            else:
                record['end'] = rec.date_from
            data_json.append(record)
        print('data_json', data_json)
        return data_json
class HrEmployee(models.Model):
    _inherit = 'hr.leave'
    attachment_id = fields.Many2many('ir.attachment', string="Documents")


    def download_uploaded_document(self):
        self.ensure_one()
        return '/web/content/%s?download=true' % self.attachment_id.id
class HrEmployee(models.Model):
    _inherit = 'hr.leave.type'


    def _get_days_request_portal(self, user_id):
        print(self.closest_allocation_to_expire.employee_id)
        self.ensure_one()
        result = self._get_employees_days_per_allocation([user_id])
        closest_allocation_remaining = 0
        if self.closest_allocation_to_expire:
            # Shows the sum of allocation expiring on the same day as the closest to expire
            employee_allocations = result[self.closest_allocation_to_expire.employee_id.id][self].items()
            closest_allocation_remaining = sum(
                res['virtual_remaining_leaves']
                for alloc, res in employee_allocations
                if alloc and alloc.date_to == self.closest_allocation_to_expire.date_to
            )
        return [self.name, {
            'remaining_leaves': ('%.2f' % self.remaining_leaves).rstrip('0').rstrip('.'),
            'virtual_remaining_leaves': ('%.2f' % self.virtual_remaining_leaves).rstrip('0').rstrip('.'),
            'max_leaves': ('%.2f' % self.max_leaves).rstrip('0').rstrip('.'),
            'leaves_taken': ('%.2f' % self.leaves_taken).rstrip('0').rstrip('.'),
            'virtual_leaves_taken': ('%.2f' % self.virtual_leaves_taken).rstrip('0').rstrip('.'),
            'leaves_requested': ('%.2f' % (self.max_leaves - self.virtual_remaining_leaves - self.leaves_taken)).rstrip(
                '0').rstrip('.'),
            'leaves_approved': ('%.2f' % self.leaves_taken).rstrip('0').rstrip('.'),
            'closest_allocation_remaining': ('%.2f' % closest_allocation_remaining).rstrip('0').rstrip('.'),
            'closest_allocation_expire': format_date(self.env,
                                                     self.closest_allocation_to_expire.date_to) if self.closest_allocation_to_expire.date_to else False,
            'request_unit': self.request_unit,
            'icon': self.sudo().icon_id.url,
        }, self.requires_allocation, self.id]

    def _get_allowed_hr_timeoff_type(self):
        type_id = self.env['hr.leave.type'].search(['|', ('requires_allocation', '=', 'no'), ('has_valid_allocation', '=', True)])
        list = []
        for rec in type_id:
            list.append([rec.id,rec.name])
        return list

    @api.model
    def get_days_all_portal(self,user_id):
        print('get_days_all_request')
        leave_types = sorted(self.search([]).filtered(lambda x: ((x.virtual_remaining_leaves > 0 or x.max_leaves))),
                             key=self._model_sorting_key, reverse=True)
        print([lt._get_days_request_portal(user_id) for lt in leave_types])

        return [lt._get_days_request_portal(user_id) for lt in leave_types]



