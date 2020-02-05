# -*- coding: utf-8 -*-
###############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>).
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
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class OpStudentCourse(models.Model):
    _name = "op.student.course"
    _description = "Student Course Details"
    _order = 'create_date desc'

    student_id = fields.Many2one('op.student', 'Student', ondelete="cascade")
    course_id = fields.Many2one('op.course', 'Course', required=True)
    batch_id = fields.Many2one('op.batch', 'Batch', required=True)
    roll_number = fields.Char('Roll Number')
    subject_ids = fields.Many2many('op.subject', string='Subjects')

    _sql_constraints = [
        ('unique_name_roll_number_id',
         'unique(roll_number,course_id,batch_id,student_id)',
         'Roll Number & Student must be unique per Batch!'),
        ('unique_name_roll_number_course_id',
         'unique(roll_number,course_id,batch_id)',
         'Roll Number must be urecnique per Batch!'),
        ('unique_name_roll_number_student_id',
         'unique(student_id,course_id,batch_id)',
         'Student must be unique per Batch!'),
    ]


class OpStudent(models.Model):
    _name = "op.student"
    _description = "Student"
    _inherits = {"res.partner": "partner_id"}

    middle_name = fields.Char('Middle Name', size=128)
    last_name = fields.Char('Last Name', size=128)
    full_name = fields.Char('Full Name', size=128, compute='compute_full_name')
    birth_date = fields.Date('Birth Date')
    gender = fields.Selection(
        [('m', 'Male'), ('f', 'Female'),
         ('o', 'Other')], 'Gender')
    nationality = fields.Many2one('res.country', 'Nationality')
    emergency_contact = fields.Many2one(
        'res.partner', 'Emergency Contact')
    visa_info = fields.Char('Visa Info', size=64)
    id_number = fields.Char('ID Card Number', size=64)
    already_partner = fields.Boolean('Already Partner')
    partner_id = fields.Many2one(
        'res.partner', 'Partner', required=True, ondelete="cascade")
    gr_no = fields.Char("GR Number", size=20)
    category_id = fields.Many2one('op.category', 'Category')
    course_detail_ids = fields.One2many('op.student.course', 'student_id',
                                        'Course Details', store=True)
    student_admission_number = fields.Char(
        'Admission Number', size=16, copy=False,
        default=lambda self: self.env['ir.sequence'].next_by_code('op.student'))
    upi_number = fields.Char('NEMIS Number', size=128)
    birth_seritificate_number = fields.Char('Birth Certificate Number', size=128)
    mmc = fields.Char(string='Memon Medical Code', copy=False, readonly=True,
                   index=True, default=lambda self: _(' '))

    _sql_constraints = [(
        'unique_gr_no',
        'unique(gr_no)',
        'GR Number must be unique per student!'
    ),(
        'unique_student_admission_number',
        'unique(student_admission_number)',
        'Admission Number Must be unique per student!'
    )]

    @api.multi
    @api.constrains('birth_date')
    def _check_birthdate(self):
        for record in self:
            if record.birth_date > fields.Date.today():
                raise ValidationError(_(
                    "Birth Date can't be greater than current date!"))

    @api.model
    def get_import_templates(self):
        return [{
            'label': _('Import Template for Students'),
            'template': '/openeducat_core/static/xls/op_student.xls'
        }]

    @api.onchange('name', 'middle_name', 'last_name')
    def compute_full_name(self):
        for rec in self:
            if rec.name and rec.middle_name and rec.last_name:
                name = (rec.name,rec.middle_name,rec.last_name)
                rec.full_name = " ".join(name)
    @api.multi
    def write(self, values):
        for rec in self:
            vals = {
                'x_admission_number': rec.student_admission_number,
                'x_gr_number': rec.gr_no,
                'x_student_id': rec.id,
            }
            self.env['res.partner'].search([('id', '=', rec.partner_id[0].id)]).write(vals)
            
        if self.mmc == ' ':
            values['mmc'] = self.env['ir.sequence'].next_by_code('op_student_mmc') or _(' ')
        
        record = super(OpStudent, self).write(values)

    @api.model
    def create(self, vals):
        vals['mmc'] = self.env['ir.sequence'].next_by_code('op_student_mmc') or _(' ')
        return super(OpStudent, self).create(vals)