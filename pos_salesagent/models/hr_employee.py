from odoo import models, fields

class AgentAnalysis(models.Model):
    _inherit = 'hr.employee'

    is_a_agent = fields.Boolean(string='Is a Sales Agent',
                                 help='Enable this field to mark the normal employee as a Sales Agent')
