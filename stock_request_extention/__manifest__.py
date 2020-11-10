# -*- coding: utf-8 -*-

# Part of Sananaz Mansuri See LICENSE file for full copyright and licensing details.

{
    'name': "Stock Request Extention",
    'version': '1.0.0',
    'license': 'Other proprietary',
    'category': 'Inventory',
    'summary': """Stock Request Extention""",
    'description': """
        Stock Request Extention
    """,
    'author': "Sananaz Mansuri",
    'website': 'www.odoo.com',
    'live_test_url': '',
    'depends': [
        'stock_request',
    ],
    'data': [
        'views/stock_request_orders_views.xml',
        'report/stock_request_orders_report.xml'
    ],
    'installable': True,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
