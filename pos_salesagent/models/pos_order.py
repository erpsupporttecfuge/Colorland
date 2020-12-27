from functools import partial

from odoo import models, api, fields

class OrderLineCommission(models.Model):
    _inherit = 'pos.order.line'

    agent_comm_amt = fields.Float('Sales Agent Commision', default=0.00)


class OrderNotes(models.Model):
    _inherit = 'pos.order'

    agent_id = fields.Many2one('hr.employee', string='Agent')
    agent_commision = fields.Float('Agent Commision (%)', default=0.00)

    @api.model

    def _order_fields(self, ui_order):
        order = super(OrderNotes, self)._order_fields(ui_order)
        process_line = partial(self.env['pos.order.line']._order_line_fields, session_id=ui_order['pos_session_id'])
        objemp = self.env['hr.employee'].search([('id', '=', ui_order['agent_id']  if "agent_id" in ui_order else False)], limit=1)
        agentcom=0.00
        if objemp:
            agentcom=objemp.sales_commision
        updated_lines = ui_order['lines']
        for rec in updated_lines:
            objproduct = self.env['product.product'].search([('id','=', rec[2]["product_id"])], limit=1)
            if objproduct:
                rec[2]["agent_comm_amt"]= objproduct.sales_agent_commision

        return {
            'user_id':      ui_order['user_id'] or False,
            'employee_id': ui_order['employee_id'] or False,
            'session_id':   ui_order['pos_session_id'],
            'lines':        [process_line(l) for l in ui_order['lines']] if ui_order['lines'] else False,
            'pos_reference': ui_order['name'],
            'sequence_number': ui_order['sequence_number'],
            'partner_id':   ui_order['partner_id'] or False,
            'date_order':   ui_order['creation_date'].replace('T', ' ')[:19],
            'fiscal_position_id': ui_order['fiscal_position_id'],
            'pricelist_id': ui_order['pricelist_id'],
            'amount_paid':  ui_order['amount_paid'],
            'amount_total':  ui_order['amount_total'],
            'amount_tax':  ui_order['amount_tax'],
            'amount_return':  ui_order['amount_return'],
            'company_id': self.env['pos.session'].browse(ui_order['pos_session_id']).company_id.id,
            'to_invoice': ui_order['to_invoice'] if "to_invoice" in ui_order else False,
            'agent_id': ui_order['agent_id']  if "agent_id" in ui_order else False,
            'agent_commision': agentcom,
        }
