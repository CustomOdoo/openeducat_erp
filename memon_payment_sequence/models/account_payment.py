# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class account_payment(models.Model):
    _inherit = 'account.payment'

    cipp_seq = fields.Char(string='CIPP Recept No.', required=True, copy=False, readonly=True,
                   index=True, default=lambda self: _('New'))
    kcpe_seq = fields.Char(string='KCPE Recept No.', required=True, copy=False, readonly=True,
                   index=True, default=lambda self: _('New'))
    kcse_seq = fields.Char(string='KCSE Recept No.', required=True, copy=False, readonly=True,
                   index=True, default=lambda self: _('New'))
    nursery_seq = fields.Char(string='Nursery Recept No.', required=True, copy=False, readonly=True,
                   index=True, default=lambda self: _('New')) 
    igcse_seq = fields.Char(string='IGCSE Recept No.', required=True, copy=False, readonly=True,
                   index=True, default=lambda self: _('New'))                                          

    @api.model
    def create(self, vals):
        if vals.get('x_studio_course') == "CIPP":
            vals['cipp_seq'] = self.env['ir.sequence'].next_by_code('account_payment_cipp') or _('New') 
        elif vals.get('x_studio_course') == "KCPE":
            vals['kcpe_seq'] = self.env['ir.sequence'].next_by_code('account_payment_kcpe') or _('New')
        elif vals.get('x_studio_course') == "KCSE":
            vals['kcse_seq'] = self.env['ir.sequence'].next_by_code('account_payment_kcse') or _('New')
        elif vals.get('x_studio_course') == "NURSERY":
            vals['nursery_seq'] = self.env['ir.sequence'].next_by_code('account_payment_nursery') or _('New')
        elif vals.get('x_studio_course') == "IGCSE":
            vals['igcse_seq'] = self.env['ir.sequence'].next_by_code('account_payment_igcse') or _('New')
        return super(account_payment, self).create(vals)
