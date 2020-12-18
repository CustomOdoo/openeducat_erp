# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class account_payment(models.Model):
    _inherit = 'account.payment'

    cipp_seq = fields.Char(string='CIPP Recept No.', required=True, copy=False, readonly=True,
                   index=True,  default='New')
    kcpe_seq = fields.Char(string='KCPE Recept No.', required=True, copy=False, readonly=True,
                   index=True,  default='New')
    kcse_seq = fields.Char(string='KCSE Recept No.', required=True, copy=False, readonly=True,
                   index=True,  default='New')
    nursery_seq = fields.Char(string='Nursery Recept No.', required=True, copy=False, readonly=True,
                   index=True,  default='New') 
    igcse_seq = fields.Char(string='IGCSE Recept No.', required=True, copy=False, readonly=True,
                   index=True,  default='New')   

    @api.model
    def create(self, vals):
        if vals.get('x_studio_course') == 'CIPP' and vals.get('cipp_seq', 'New') == 'New':
            vals['cipp_seq'] = self.env['ir.sequence'].next_by_code('account_payment_cipp') or 'New' 
        elif vals.get('x_studio_course') == "KCPE" and vals.get('kcpe_se', 'New') == 'New':
            vals['kcpe_seq'] = self.env['ir.sequence'].next_by_code('account_payment_kcpe') or 'New'
        elif vals.get('x_studio_course') == "KCSE" and vals.get('kcse_seq', 'New') == 'New':
            vals['kcse_seq'] = self.env['ir.sequence'].next_by_code('account_payment_kcse') or 'New'
        elif vals.get('x_studio_course') == "NURSERY" and vals.get('nursery_sq', 'New') == 'New':
            vals['nursery_seq'] = self.env['ir.sequence'].next_by_code('account_payment_nursery') or 'New'
        elif vals.get('x_studio_course') == "IGCSE" and vals.get('igcse_seq', 'New') == 'New':
            vals['igcse_seq'] = self.env['ir.sequence'].next_by_code('account_payment_igcse') or 'New'
        return super(account_payment, self).create(vals)