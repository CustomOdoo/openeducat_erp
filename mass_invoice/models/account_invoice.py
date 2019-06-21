from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice.line'

    @api.onchange('product_id', 'invoice_id.partner_id')
    def compute_memon_discount(self):
        for record in self:
            if record.product_id and record.invoice_id.partner_id.x_student_id.x_studio_is_member is True:
                record.discount = (record.product_id.memon_discount / 
                    record.product_id.lst_price) * 100