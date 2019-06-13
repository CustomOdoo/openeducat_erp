from odoo import models, api, fields, _ 


class FeeStructure(models.Model):
    _name = 'op.fee.structure'
    _description = 'Fee Structure'
    _inherit = 'mail.thread'

    name = fields.Char('Name')
    product = fields.Many2many('product.template', string='Product', required=True,
        domain=[('type', '=', 'service')], track_visibility='onchange')
    total = fields.Float('Total', compute='compute_fee_stucture')
    memon_fee = fields.Float('Memon Fee', compute='compute_memon_fee')
    memon_discount = fields.Float('Memon Discount', compute='compute_memon_discount')

    @api.onchange('product')
    @api.depends('product')
    def compute_fee_stucture(self):
        for record in self:
            record.total = sum(record.mapped('product.list_price'))
            record.memon_fee = sum(record.mapped('product.memon_fee'))
            record.memon_discount = sum(record.mapped('product.memon_discount'))