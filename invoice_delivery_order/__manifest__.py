# -*- coding: utf-8 -*-
{
    'name' : 'Auto Create Delivery Order from Invoice',
    'version' : '16.0.1.0.0',
    'author' : 'Ohia Ikenna Markhenry',
    'category': 'Accounting',
    'website': 'https://bitlect.net',
    'price': 15.99,
    'currency': 'USD',
    'summary': 'Odoo module that automatically creates delivery orders from invoices. When an invoice is validated, it will create stock pickings and moves for the products in the invoice lines',
    'description': """
        """,
    'depends' : ['base','account','stock','sale'],
    'data': ['views/view_invoice_form.xml'],
    'assets': {
        'web.assets_backend': []
    },
    'demo': [],
    'qweb': [],
    'js':[],
    'installable': True,
    'application': True,
    'auto_install': False,
    'sequence':2,
    'license': 'Other proprietary',
}
