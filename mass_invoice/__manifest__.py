# -*- coding: utf-8 -*-
{
    'name': "Mass Invoicing",

    'summary': """
        One click Mass Invoicing
    """,

    'description': """
        This module, One click Mass Invoicing, allows you to create invoices in bulk. 
        
        A good use case would be: 
        You want to charge students (eg class five students) for trip fee, the default/normal way is 
        for you to create an invoice for each student separately. <-- This is tiresome!!! 
        
        This module you to create all the invoices with one click""",

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