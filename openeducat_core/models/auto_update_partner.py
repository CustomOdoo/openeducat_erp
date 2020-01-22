from odoo import models, api, fields


class AutoUpdatePartner(models.Model):
    _name = 'op.autoupdate_partner'
    _description = "Auto update Partner"

    student_ids = fields.Many2many('op.student', string='Students')
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')], 
        string='Status', default='draft')

    @api.depends('student_ids')
    def auto_update_partner(self):
        for record in self:
            if record.student_ids:
                for rec in record.student_ids:
                    vals = {
                        'x_admission_number': rec.student_admission_number,
                        'x_gr_number': rec.gr_no,
                        'x_student_id': rec.id,
                    }
                    self.env['res.partner'].search([('id', '=', rec.partner_id[0].id)]).write(vals)