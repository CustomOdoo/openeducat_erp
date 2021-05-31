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
from datetime import datetime
from datetime import timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

class OpExamSession(models.Model):
    _name = "op.exam.session"
    _inherit = ["mail.thread"]
    _description = "Exam Session"

    name = fields.Char(
        'Exam Session', size=256, required=True, track_visibility='onchange')
    course_id = fields.Many2one(
        'op.course', 'Course', required=True, track_visibility='onchange')
    batch_id = fields.Many2one(
        'op.batch', 'Batch', required=True, track_visibility='onchange')
    exam_code = fields.Char(
        'Exam Session Code', size=16,
        required=True, track_visibility='onchange')
    start_date = fields.Date(
        'Start Date', required=True, track_visibility='onchange')
    end_date = fields.Date(
        'End Date', required=True, track_visibility='onchange')
    exam_ids = fields.One2many(
        'op.exam', 'session_id', 'Exam(s)')
    exam_type = fields.Many2one(
        'op.exam.type', 'Exam Type',
        required=True, track_visibility='onchange')
    evaluation_type = fields.Selection(
        [('normal', 'Normal'), ('grade', 'Grade')],
        'Evaluation type', default="grade",
        required=True, track_visibility='onchange')
    venue = fields.Many2one(
        'res.partner', 'Venue', track_visibility='onchange')
    # total_exam_students = fields.Integer("Total Exam Student", 
    #     compute='_compute_total_exam_students', store=True)

    # @api.multi
    # @api.depends()
    # def _compute_total_exam_students(self):
    #     for record in self:
    #         record.total_exam_students = len(record.exam_ids.attendees_line.ids)

    _sql_constraints = [
        ('unique_exam_session_code',
         'unique(exam_code)', 'Code should be unique per exam session!')]

    @api.onchange('course_id', 'batch_id', 'exam_type', 'x_studio_term', 'start_date')
    def _compute_session_name(self):
        for record in self:
            if record.course_id and record.batch_id and record.exam_type and record.x_studio_term:
                # date = datetime.strptime(record.start_date, DEFAULT_SERVER_DATE_FORMAT).year
                record.name = "Exam Session for %s %s %s - %s" % (record.course_id.name, 
                    record.batch_id.name, record.exam_type.name, record.x_studio_term.x_name)

    @api.constrains('start_date', 'end_date')
    def _check_date_time(self):
        if self.start_date > self.end_date:
            raise ValidationError(
                _('End Date cannot be set before Start Date.'))

    @api.onchange('course_id')
    def onchange_course(self):
        self.batch_id = False

    @api.model
    def create(self, values):
        record = super(OpExamSession, self).create(values)

        subjects = self.env['op.subject'].search([('x_studio_course', '=', self.course_id.id)])
        for subject in subjects:
            self.env['op.exam'].create({
                'session_id': self.id,
                'course_id': self.course_id,
                'batch_id': self.batch_id,
                'subject_id': subject.id,
                'exam_code': subject.code,
                # 'attendees_line': ,
                'start_time': datetime.now(),
                'end_time': datetime.now() + timedelta(hours=2),
                # 'exam_paper': ,
                # 'state': ,
                # 'responsible_id': ,
                'name': subject.name,
                'total_marks': 100,
                'min_marks': 50,
                # 'total_attendees': ,
            })
        return record
