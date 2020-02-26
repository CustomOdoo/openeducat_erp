# -*- coding: utf-8 -*-
{
    'name': "Memon Payment Sequence",

    'summary': """
        Receipt serial numbers""",

    'description': """
        Payment Sequence for the different MEMON Carricula.
    """,

    'author': "AthmanZiri",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/course_sequnce.xml',
        'views/account_payment.xml',
    ],
}