# -*- coding: utf-8 -*-
{
    'name': "Mass Invoice",

    'summary': """
        Mass Invoice""",

    'description': """
        Mass Invoice
    """,

    'author': "AthmanZiri",
    'website': "https://www.innovus.co.ke",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Education',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'product'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/mass_invoice.xml',
    ],
    'installable': True,
    'application': True,
}