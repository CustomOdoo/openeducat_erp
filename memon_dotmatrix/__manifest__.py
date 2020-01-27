# -*- coding: utf-8 -*-
{
    'name': "Dotmatrix Printer",

    'summary': """
        Dotmatrix printer addon""",

    'description': """
        Dotmatrix printer integration for Odoo
    """,

    'author': "Akhmad Daniel Sembiring",
    'website': "http://www.vitraining.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],
    # 'depends': ['base', 'account', 'purchase', 'stock', 'sale_management'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/templates.xml',
        'views/invoice.xml',
        'views/assets.xml',
        'views/account_payment.xml',
        # 'views/po.xml',
        # 'views/picking.xml',
        # 'views/sale.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}