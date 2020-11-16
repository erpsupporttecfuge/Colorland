# -*- coding: utf-8 -*-

from odoo import models, fields


class StockRequestOrder(models.Model):
    _inherit = 'stock.request.order'

    route_id = fields.Many2one(
        'stock.location.route',
        string='Route',
    )
    request_type = fields.Many2one('stock.request.type', 'Request Type', required="1")
    to_location_id = fields.Many2one(
        'stock.location', 'To Location',
        readonly=True, required=True,
        domain="[('usage','=','internal'), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        states={'draft': [('readonly', False)]}, check_company=True,
        help="Location where the system will stock the finished products.")
    remarks = fields.Text('Remark')


class StockRequest(models.Model):
    _inherit = 'stock.request'

    #inherit to remove Domain
    route_id = fields.Many2one(
        domain=[],
    )

    def _action_confirm(self):
        self.state = 'open'

class StockRequestType(models.Model):
    _name ='stock.request.type'
    _description ='Stock Request Type'

    name = fields.Char('Request Type')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
