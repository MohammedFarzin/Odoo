from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = 'mail.thread'
    _description = 'Patient Records'

    name = fields.Char(string='Name', required=True, tracking=True)
    age = fields.Integer(string='Age', tracking=True)
    is_child = fields.Boolean(string='Is Child ?', tracking=True)
    notes = fields.Text(string='Notes')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('others', 'Others')], string='Gender',
                              tracking=True)
    capitilized_name = fields.Char(string='Capitalized name', compute='_compute_capitilized_name', store=True)
    ref = fields.Char(string='Reference', default=lambda self: _('New'))

    @api.model_create_multi
    def create(self, val_list):
        for vals in val_list:
            vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient, self).create(val_list)

    @api.constrains('is_child', 'age')
    def _check_child_age(self):
        for record in self:
            if self.is_child and self.age == 0:
                raise ValidationError(_('Age has to be recorded'))

    @api.depends('name')
    def _compute_capitilized_name(self):
        for record in self:
            if record.name:
                record.capitilized_name = record.name.upper()
            else:
                record.capitilized_name = ''

    @api.onchange('age')
    def _onchange_age(self):
        if self.age <= 10:
            self.is_child = True
        else:
            self.is_child = False
