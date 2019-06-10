from odoo import models, api, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    memon_discount = fields.Float('Memon Discount', compute='compute_memon_discount')
    memon_fee = fields.Float('Memon Fee')

    @api.onchange('list_price', 'memon_fee')
    def compute_memon_discount(self):
        for rec in self:
            if rec.memon_fee:
                rec.memon_discount = rec.list_price - rec.memon_fee