from odoo import api, exceptions, fields, models, _
from datetime import datetime








class ResDocumentsType(models.Model):
    _name ="res.document.type"
    name=fields.Char(string="name",require=True)
    is_mandatory = fields.Boolean(string="Is Mandatory")
    remainder_days = fields.Integer(string="Notification Time")
class ResDocuments(models.Model):
    _name = 'res.document'

    employee_id = fields.Many2one('hr.employee',string="Employee")
    document_type_id = fields.Many2one('res.document.type',string="Document Type")
    date_of_expire = fields.Date(string="Date of Expire")
    attachment_id = fields.Many2many('ir.attachment', string="Attachment" )
    status = fields.Selection([('valid', 'Valid'), ('expired', 'Expired')],compute="_compute_expire_status")


    def get_documents_table_in_portal(self,user_id):
        print(user_id)
        return  self.search([('employee_id.user_id','=',user_id)])



    def download_uploaded_document(self):
        self.ensure_one()
        return '/web/content/%s?download=true' % self.attachment_id.id
    @api.depends('date_of_expire')
    def _compute_expire_status(self):
        for rec in self:
            if rec.date_of_expire:
                if rec.date_of_expire > fields.Date.today():
                    rec.status = 'valid'
                else:
                    rec.status = 'expired'
            else:
                rec.status ='valid'
class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    documents_ids = fields.One2many('res.document','employee_id',string="Documents")

