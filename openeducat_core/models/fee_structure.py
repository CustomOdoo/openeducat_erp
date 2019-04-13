from odoo import models, api, fields, _ 


class FeeStructure(models.Model):
    _name = 'op.fee.structure'
    _description = 'Fee Structure'
    _inherit = 'mail.thread'

    name = fields.Char('Name')
    product = fields.Many2many('product.template', string='Product', required=True,
        domain=[('type', '=', 'service')], track_visibility='onchange')
    total = fields.Float('Total', compute='compute_fee_stucture')

    @api.onchange('product')
    @api.depends('product')
    def compute_fee_stucture(self):
        for record in self:
            record.total = sum(record.mapped('product.list_price'))