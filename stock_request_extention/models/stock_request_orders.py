# -*- coding: utf-8 -*-

from odoo import models, fields


class StockRequestOrder(models.Model):
    _inherit = 'stock.request.order'

    route_id = fields.Many2one(
        'stock.location.route',
        string='Route',
    )

    remarks = fields.Text('Remark')


class StockRequest(models.Model):
    _inherit = 'stock.request'

    #inherit to remove Domain
    route_id = fields.Many2one(
        domain=[],
    )

    def _action_confirm(self):
        self.state = 'open'

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
