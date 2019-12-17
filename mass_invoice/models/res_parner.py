from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    pledge_active = fields.Boolean("Pledge Active", default=False, 
        compute='_compute_pledge_active')

    @api.multi
    def _compute_pledge_active(self):
        for record in self:
            pledges = self.env['x_student_pledges'].search([
                ('x_studio_field_ypSrC.partner_id.name', '=', record.name), 
                ('x_studio_field_ypSrC.partner_id.id', '=', record.id)])
            for pledge in pledges:
                if pledge.x_studio_status == "Active":
                    record.pledge_active = True
                    break