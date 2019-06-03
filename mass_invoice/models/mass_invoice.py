# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime


class MassInvoice(models.Model):
    _name = 'op.mass.invoice'
    _description = 'Mass Invoice'

    student_ids = fields.Many2many('op.student', string='Students')
    product_id = fields.Many2one('product.template', string='Products')
    invoice_id = fields.Many2one('account.invoice', 'Invoice')
    amount = fields.Float('Fees Amount', related='product_id.lst_price')
    date = fields.Date('Submit Date', default=fields.Date.today())
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')], 
        string='Status', default='draft')
    memon_discount = fields.Float('Memon Discount', related='product_id.memon_discount')

    @api.depends('student_ids', 'product_id')
    def create_invoices(self):
        for record in self:
            if record.student_ids:
                for rec in record.student_ids:
                    inv_obj = self.env['account.invoice']
                    partner_id = rec.partner_id
                    student = rec
                    account_id = False
                    product = record.product_id
                    if product.property_account_income_id:
                        account_id = product.property_account_income_id.id
                    if not account_id:
                        account_id = product.categ_id.property_account_income_categ_id.id
                    if not account_id:
                        raise UserError(
                            _('There is no income account defined for this product: "%s".'
                            'You may have to install a chart of account from Accounting'
                            ' app, settings menu.') % product.name)
                    if self.amount <= 0.00:
                        raise UserError(
                            _('The value of the deposit amount must be positive.'))
                    else:
                        amount = self.amount
                        name = product.name

                    if student.x_studio_is_member == True:
                        discount = (product.memon_discount / amount) * 100
                    else:
                        discount = 0.0
                    
                    invoice = inv_obj.create({
                        'name': student.name,
                        'origin': student.gr_no or False,
                        'type': 'out_invoice',
                        'reference': False,
                        'account_id': partner_id.property_account_receivable_id.id,
                        'partner_id': partner_id.id,
                        'invoice_line_ids': [(0, 0, {
                            'name': name,
                            'origin': student.gr_no,
                            'account_id': account_id,
                            'price_unit': amount,
                            'quantity': 1.0,
                            'discount': discount,
                            'uom_id': product.uom_id.id,
                            'product_id': product.id,
                        })],
                    })
                    invoice.compute_taxes()
                    invoice.action_invoice_open()
                    self.state = 'done'
                    self.invoice_id = invoice.id
        return True
