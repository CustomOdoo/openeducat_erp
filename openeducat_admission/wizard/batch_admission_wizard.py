from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class BatchAdmissionWizard(models.TransientModel):
    """ Student Admission in bulk/batches. 
        To be used for previously terminated students
    """
    _name = 'op.batch.admission'
    _description = 'Batch admission'
    _order = 'create_date desc'

    fees = fields.Float('Fees')
    fees_term_id = fields.Many2one('op.fees.terms', 'Fees Term')
    # nbr = fields.Integer('No of Admission', readonly=True)
    register_id = fields.Many2one(
        'op.admission.register', 'Admission Register', required=True)
    course_id = fields.Many2one('op.course', 'Course', required=True)
    batch_id = fields.Many2one('op.batch', 'Batch', required=True)
    students = fields.Many2many('op.student', 'Students', 
        domain=[('active', '=', False)])

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
    def mass_enroll(self):
        print("Hello WORLD **********************************************")
        for record in self:
            print("*****************8",record)
            for sd in record.students:
                print("#############", sd)
                vals = {
                    'name': sd.name,
                    'birth_date': sd.birth_date,
                    'gender': sd.gender,
                    'image': sd.image or False,
                    'street': sd.street or False,
                    'street2': sd.street2 or False,
                    'phone': sd.phone or False,
                    'mobile': sd.mobile or False,
                    'email': sd.email or False,
                    'zip': sd.zip or False,
                    'city': sd.city or False,
                    'country_id': sd.country_id and sd.country_id.id or False,
                    'state_id': sd.state_id and sd.state_id.id or False,
                    'partner_id': sd.partner_id and sd.partner_id.id or False,
                    'course_id': student.course_id and student.course_id.id or False,
                    'batch_id': student.batch_id and student.batch_id.id or False,
                    'is_student': True
                }
                pprint("$$$$$$$$$$$$$$", vals)
                print(hello)
                admission = self.env['op.admission'].create(vals)
                # admission.admission_confirm()
                admission.enroll_student()