from odoo import models, api, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    memon_discount = fields.Float('Memon Discount')