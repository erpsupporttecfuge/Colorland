# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockRequestOrder(models.Model):
    _inherit = "stock.request.order"

    custom_stock_request_order_submitted = fields.Boolean(
        string='Request Submitted',
        copy=False,
        readonly=True,
    )
    
    def action_custom_submitted(self):
        for rec in self:
            rec.custom_stock_request_order_submitted = True
    
    def action_cancel(self):
        res = super(StockRequestOrder, self).action_cancel()
        if res:
            self.custom_stock_request_order_submitted = False
        return res

