from odoo import models, api, fields, _


class payment(models.Model):
    _inherit = 'account.payment'

    printer_data = fields.Text("Printer Data", readonly=True)

    @api.multi
    def action_refresh_printer_data(self):
        tmpl = self.env['mail.template'].search([('name','=','Dot Matrix Payment')])
        data = tmpl._render_template( tmpl.body_html, 'account.payment', self.id )
        self.printer_data = data

    @api.multi
    def dummy(self):
        pass


    @api.multi
    def post(self):
        res = super(payment, self).post()
        self.action_refresh_printer_data()
        return res