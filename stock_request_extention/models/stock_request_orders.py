# -*- coding: utf-8 -*-

from odoo import models, fields


class StockRequestOrder(models.Model):
    _inherit = 'stock.request.order'

    route_id = fields.Many2one(
        'stock.location.route',
        string='Route',
    )


class StockRequest(models.Model):
    _inherit = 'stock.request'

    #inherit to remove Domain
    route_id = fields.Many2one(
        domain=[],
    )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
