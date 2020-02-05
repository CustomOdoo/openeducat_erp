# -*- coding: utf-8 -*-
##############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech Receptives(<http://www.techreceptives.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class OpAdmission(models.Model):
    _name = "op.admission"
    _inherit = "mail.thread"
    _rec_name = "application_number"
    _order = "application_number desc"
    _description = "Admission"

    name = fields.Char(
        'Full Name', size=128, required=True,
        states={'done': [('readonly', True)]})
    middle_name = fields.Char(
        'Middle Name', size=128,
        states={'done': [('readonly', True)]})
    last_name = fields.Char(
        'Last Name', size=128, 
        states={'done': [('readonly', True)]})
    full_name = fields.Char(
        'Full Name', size=128, required=True, compute='compute_full_name',
        states={'done': [('readonly', True)]})
    title = fields.Many2one(
        'res.partner.title', 'Title', states={'done': [('readonly', True)]})
    application_number = fields.Char(
        'Application Number', size=16, required=True, copy=False,
        states={'done': [('readonly', True)]},
        default=lambda self:
        self.env['ir.sequence'].next_by_code('op.admission'))
    admission_date = fields.Date(
        'Admission Date', copy=False,
        states={'done': [('readonly', True)]})
    application_date = fields.Datetime(
        'Application Date', required=True, copy=False,
        states={'done': [('readonly', True)]},
        default=lambda self: fields.Datetime.now())
    birth_date = fields.Date(
        'Birth Date', required=True, states={'done': [('readonly', True)]})
    course_id = fields.Many2one(
        'op.course', 'Course', required=True,
        states={'done': [('readonly', True)]})
    batch_id = fields.Many2one(
        'op.batch', 'Batch', required=False,
        states={'done': [('readonly', True)],
                'submit': [('required', True)],
                'fees_paid': [('required', True)]})
    street = fields.Char(
        'Street', size=256, states={'done': [('readonly', True)]})
    street2 = fields.Char(
        'Street2', size=256, states={'done': [('readonly', True)]})
    phone = fields.Char(
        'Phone', size=16, states={'done': [('readonly', True)]})
    mobile = fields.Char(
        'Mobile', size=16,
        states={'done': [('readonly', True)], 'submit': [('required', True)]})
    email = fields.Char(
        'Email', size=256,
        states={'done': [('readonly', True)]})
    city = fields.Char('City', size=64, states={'done': [('readonly', True)]})
    zip = fields.Char('Zip', size=8, states={'done': [('readonly', True)]})
    state_id = fields.Many2one(
        'res.country.state', 'States', states={'done': [('readonly', True)]})
    country_id = fields.Many2one(
        'res.country', 'Country', states={'done': [('readonly', True)]})
    fees = fields.Float('Fees', states={'done': [('readonly', True)]})
    image = fields.Binary('image', states={'done': [('readonly', True)]})
    state = fields.Selection(
        [('draft', 'Draft'), ('submit', 'Submitted'),
         ('confirm', 'Confirmed'), ('admission', 'Waiting Class'),
         ('reject', 'Rejected'), ('pending', 'Pending'),
         ('cancel', 'Cancelled'), ('done', 'Done')],
        'State', default='draft', track_visibility='onchange')
    due_date = fields.Date('Due Date', states={'done': [('readonly', True)]})
    prev_institute_id = fields.Many2one(
        'res.partner', 'Previous Institute',
        states={'done': [('readonly', True)]})
    prev_course_id = fields.Many2one(
        'op.course', 'Previous Course', states={'done': [('readonly', True)]})
    prev_result = fields.Char(
        'Previous Result', size=256, states={'done': [('readonly', True)]})
    family_business = fields.Char(
        'Family Business', size=256, states={'done': [('readonly', True)]})
    family_income = fields.Float(
        'Family Income', states={'done': [('readonly', True)]})
    gender = fields.Selection(
        [('m', 'Male'), ('f', 'Female'), ('o', 'Other')],
        string='Gender',
        required=True,
        states={'done': [('readonly', True)]})
    student_id = fields.Many2one(
        'op.student', 'Student', states={'done': [('readonly', True)]})
    nbr = fields.Integer('No of Admission', readonly=True)
    register_id = fields.Many2one(
        'op.admission.register', 'Admission Register', required=True,
        states={'done': [('readonly', True)]})
    partner_id = fields.Many2one('res.partner', 'Partner')
    is_student = fields.Boolean('Is Already Student')
    fees_term_id = fields.Many2one('op.fees.terms', 'Fees Term')
    upi_number = fields.Char('NEMIS Number', size=128)
    birth_seritificate_number = fields.Char('Birth Certificate Number', size=128)
    gr_no = fields.Char("GR Number", size=20)
    religion = fields.Many2one('x_religion', 'Religion')

    @api.onchange('student_id', 'is_student')
    def onchange_student(self):
        if self.is_student and self.student_id:
            sd = self.student_id
            self.title = sd.title and sd.title.id or False
            self.name = sd.name
            self.birth_date = sd.birth_date
            self.gender = sd.gender
            self.image = sd.image or False
            self.street = sd.street or False
            self.street2 = sd.street2 or False
            self.phone = sd.phone or False
            self.mobile = sd.mobile or False
            self.email = sd.email or False
            self.zip = sd.zip or False
            self.city = sd.city or False
            self.religion = sd.x_studio_religion or False
            self.country_id = sd.country_id and sd.country_id.id or False
            self.state_id = sd.state_id and sd.state_id.id or False
            self.partner_id = sd.partner_id and sd.partner_id.id or False
            self.x_studio_is_member = sd.x_studio_is_member or False
        else:
            self.title = ''
            self.name = ''
            self.birth_date = ''
            self.gender = ''
            self.image = False
            self.street = ''
            self.street2 = ''
            self.phone = ''
            self.mobile = ''
            self.zip = ''
            self.city = ''
            self.country_id = False
            self.state_id = False
            self.partner_id = False

    @api.onchange('register_id')
    def onchange_register(self):
        self.course_id = self.register_id.course_id
        self.fees = self.register_id.fee_structure_id.total

    @api.onchange('course_id')
    def onchange_course(self):
        self.batch_id = False
        term_id = False
        if self.course_id and self.course_id.fees_term_id:
            term_id = self.course_id.fees_term_id.id
        self.fees_term_id = term_id

    @api.multi
    @api.constrains('register_id', 'application_date')
    def _check_admission_register(self):
        for rec in self:
            start_date = fields.Date.from_string(rec.register_id.start_date)
            end_date = fields.Date.from_string(rec.register_id.end_date)
            application_date = fields.Date.from_string(rec.application_date)
            if application_date < start_date or application_date > end_date:
                raise ValidationError(_(
                    "Application Date should be between Start Date & \
                    End Date of Admission Register."))

    @api.multi
    @api.constrains('birth_date')
    def _check_birthdate(self):
        for record in self:
            if record.birth_date > fields.Date.today():
                raise ValidationError(_(
                    "Birth Date can't be greater than current date!"))

    @api.multi
    def submit_form(self):
        self.state = 'submit'

    @api.multi
    def admission_confirm(self):
        """
            Put newly confirmed students to waiting class
        """
        for record in self:
            if not record.partner_id:
                student_user = self.env['res.users'].create({
                    'name': record.name,
                    'login': record.email,
                    'image': self.image or False,
                    'company_id': self.env.ref('base.main_company').id,
                    'groups_id': [
                        (6, 0,
                        [self.env.ref('openeducat_core.group_op_student').id])]
                })
                details = {
                    'phone': record.phone,
                    'mobile': record.mobile,
                    'email': record.email,
                    'street': record.street,
                    'street2': record.street2,
                    'city': record.city,
                    'country_id':
                        record.country_id and record.country_id.id or False,
                    'state_id': record.state_id and record.state_id.id or False,
                    'image': record.image,
                    'zip': record.zip,
                    'customer': True,
                }
                student_user.partner_id.write(details)
                self.partner_id = student_user.partner_id

            self.state = 'admission'
            

    @api.multi
    def confirm_in_progress(self):
        for record in self:
            record.state = 'confirm'

    @api.multi
    def get_student_vals(self):
        for student in self:
            
            details = {
                'phone': student.phone,
                'mobile': student.mobile,
                'email': student.email,
                'street': student.street,
                'street2': student.street2,
                'city': student.city,
                'country_id':
                    student.country_id and student.country_id.id or False,
                'state_id': student.state_id and student.state_id.id or False,
                'zip': student.zip,
                'title': student.title and student.title.id or False,
                'name': student.name,
                'birth_date': student.birth_date,
                'gender': student.gender,
                'course_id': student.course_id and student.course_id.id or False,
                'batch_id': student.batch_id and student.batch_id.id or False,
                'image': student.image or False,
                'course_detail_ids': [[0, False, {
                    'date': fields.Date.today(),
                    'course_id':
                        student.course_id and student.course_id.id or False,
                    'batch_id':
                        student.batch_id and student.batch_id.id or False,
                }]],
                'upi_number': student.upi_number,
                'gr_no': student.gr_no,
                'birth_seritificate_number': student.birth_seritificate_number,
                'religion': student.religion,
                # 'user_id': student_user.id,
                'partner_id': student.partner_id.id,
                'x_studio_is_member': student.x_studio_is_member,
                'x_studio_parent_name': student.x_studio_parent_name,
                'x_studio_guardian_id_no': student.x_studio_guardian_id_no,
                'x_studio_occupation': student.x_studio_occupation,
                'x_studio_relationship_to_child_1': student.x_studio_relationship_to_child,
                'x_studio_previous_school': student.prev_institute_id.name,
                'x_studio_house': student.x_studio_house,
                'x_studio_index_number': student.x_studio_index_number,
                'x_studio_previous_result': student.prev_result,
            }
            return details

    @api.multi
    def enroll_student(self):
        for record in self:
            total_admission = self.env['op.admission'].search_count(
                [('register_id', '=', record.register_id.id),
                 ('state', '=', 'done')])
            if record.register_id.max_count:
                if not total_admission < record.register_id.max_count:
                    msg = 'Max Admission In Admission Register :- (%s)' % (
                        record.register_id.max_count)
                    raise ValidationError(_(msg))
            if not record.student_id:
                vals = record.get_student_vals()
                student_id = self.env['op.student'].create(vals).id
            else:
                student_id = record.student_id.id
                record.student_id.write({
                    'active': True,
                    'x_studio_religion': record.religion.id,
                    'x_studio_terminated': False,
                    'upi_number': record.upi_number,
                    'gr_no': record.gr_no,
                    'birth_seritificate_number': record.birth_seritificate_number,
                    'course_detail_ids': [[0, False, {
                        'date': fields.Date.today(),
                        'course_id':
                            record.course_id and record.course_id.id or False,
                        'batch_id':
                            record.batch_id and record.batch_id.id or False,
                    }]],
                })
            record.write({
                'nbr': 1,
                'state': 'done',
                'admission_date': fields.Date.today(),
                'student_id': student_id,
            })
            reg_id = self.env['op.subject.registration'].create({
                'student_id': student_id,
                'batch_id': record.batch_id.id,
                'course_id': record.course_id.id,
                'min_unit_load': record.course_id.min_unit_load or 0.0,
                'max_unit_load': record.course_id.max_unit_load or 0.0,
                'state': 'draft',
            })
            reg_id.get_subjects()

            """
                Create Enrollment Activity in student profile
            """
            activity_type = self.env["op.activity.type"]
            act_type = activity_type.search(
                [('name', '=', 'Enrollment')], limit=1)
            if not act_type:
                act_type = activity_type.create({'name': 'Enrollment'})
            activity_vals = {
                'student_id': student_id,
                'type_id': act_type.id,
                'date': fields.Date.today(),
                'description': 'Enrolled to ' + record.batch_id.name
            }
            self.env['op.activity'].create(activity_vals)

            """ Create invoice for fee payment process of student """

            inv_obj = self.env['account.invoice']
            partner_id = record.partner_id
            account_id = False
            product_ids = record.register_id.fee_structure_id.product.ids

            for prod_id in product_ids:
                product = self.env['product.template'].search([('id', '=', prod_id)])[0]
                if product:
                    account_id = product.property_account_income_id.id
                if not account_id:
                    account_id = product.categ_id.property_account_income_categ_id.id
                if not account_id:
                    raise UserError(
                        _('There is no income account defined for this product: "%s". \
                        You may have to install a chart of account from Accounting \
                        app, settings menu.') % (product.name,))

                if self.fees <= 0.00:
                    raise UserError(
                        _('The value of the deposit amount must be positive.'))
                else:
                    amount = product.lst_price
                    name = product.name
                
                if self.x_studio_is_member == True:
                    discount = (product.memon_discount / amount) * 100
                else:
                    discount = 0.0
                
                invoice = inv_obj.create({
                    'name': product.name,
                    'origin': self.application_number,
                    'type': 'out_invoice',
                    'reference': False,
                    'account_id': partner_id.property_account_receivable_id.id,
                    'partner_id': partner_id.id,
                    'invoice_line_ids': [(0, 0, {
                        'name': name,
                        'origin': self.application_number,
                        'account_id': account_id,
                        'price_unit': product.lst_price,
                        'quantity': 1.0,
                        'discount': discount,
                        'uom_id': product.uom_id.id,
                        'product_id': product.id,
                    })],
                })
                invoice.compute_taxes()
                invoice.action_invoice_open()

    @api.multi
    def confirm_rejected(self):
        self.state = 'reject'

    @api.multi
    def confirm_pending(self):
        self.state = 'pending'

    @api.multi
    def confirm_to_draft(self):
        self.state = 'draft'

    @api.multi
    def confirm_cancel(self):
        self.state = 'cancel'

    @api.multi
    def payment_process(self):
        self.state = 'fees_paid'

    @api.multi
    def open_student(self):
        form_view = self.env.ref('openeducat_core.view_op_student_form')
        tree_view = self.env.ref('openeducat_core.view_op_student_tree')
        value = {
            'domain': str([('id', '=', self.student_id.id)]),
            'view_type': 'form',
            'view_mode': 'tree, form',
            'res_model': 'op.student',
            'view_id': False,
            'views': [(form_view and form_view.id or False, 'form'),
                      (tree_view and tree_view.id or False, 'tree')],
            'type': 'ir.actions.act_window',
            'res_id': self.student_id.id,
            'target': 'current',
            'nodestroy': True
        }
        self.state = 'done'
        return value