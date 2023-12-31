# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from dateutil.relativedelta import relativedelta
from datetime import datetime

class ACSHmsMixin(models.AbstractModel):
    _name = "acs.hms.mixin"
    _description = "HMS Mixin"

    @api.model
    def acs_create_invoice(self, patient, product_data, inv_data={}):
        invoice = self.env['account.move'].create({
            'partner_id': patient.partner_id.id,
            'patient_id': patient.id,
            'move_type': 'out_invoice',
            'ref': self.name,
            'currency_id': self.env.user.company_id.currency_id.id,
            'invoice_line_ids': self.acs_get_invoice_lines(product_data, patient),
            'ref_physician_id': inv_data.get('ref_physician_id',False),
            'physician_id': inv_data.get('physician_id',False),
        })
        invoice._onchange_partner_id()

        for line in invoice.invoice_line_ids:
            # line._get_computed_name()
            # line._get_computed_account()
            line._get_computed_taxes()
            # line._get_computed_uom()
        return invoice

    @api.model
    def acs_get_invoice_lines(self, product_data, patient):
        lines = []
        for data in product_data:
            product = data.get('product_id')
            if product:
                if not data.get('price_unit') and patient.property_product_pricelist:
                    price = product.with_context(pricelist=patient.property_product_pricelist.id).list_price
                else:
                    price = data.get('price_unit', product.list_price)
                lines.append((0, 0, {
                    'name': data.get('name',product.name),
                    'product_id': product.id,
                    'price_unit': price,
                    'quantity': data.get('quantity',1.0),
                    'discount': data.get('discount',0.0),
                    'product_uom_id': data.get('product_uom_id',product.uom_id.id),
                    # 'analytic_account_id': data.get('account_analytic_id',False),
                }))
            else:
                lines.append((0, 0, {
                    'name': data.get('name'),
                    'display_type': 'line_section',
                }))
                
        return lines

    def acs_action_view_invoice(self, invoices):
        action = self.env.ref('account.action_move_out_invoice_type').read()[0]
        if len(invoices) > 1:
            action['domain'] = [('id', 'in', invoices.ids)]
        elif len(invoices) == 1:
            action['views'] = [(self.env.ref('account.view_move_form').id, 'form')]
            action['res_id'] = invoices.id
        else:
            action = {'move_type': 'ir.actions.act_window_close'}

        context = {
            'default_move_type': 'out_invoice',
        }
        action['context'] = context
        return action

    def consume_material(self, source_location_id, dest_location_id, product_data):
        product = product_data['product']
        move = self.env['stock.move'].create({
            'name' : product.name,
            'product_id': product.id,
            'product_uom': product.uom_id.id,
            'product_uom_qty': product_data.get('qty',1.0),
            'date': product_data.get('date',fields.datetime.now()),
            'date_expected': fields.datetime.now(),
            'location_id': source_location_id,
            'location_dest_id': dest_location_id,
            'state': 'draft',
            'origin': self.name,
            'quantity_done': product_data.get('qty',1.0),
        })
        move._action_confirm()
        move._action_assign()
        if move.state == 'assigned':
            move._action_done()
        return move


class ResPartner(models.Model):
    _inherit= "res.partner"

    @api.depends('birthday', 'date_of_death')
    def _get_age(self):
        for rec in self:
            age = ''
            if rec.birthday:
                end_data = rec.date_of_death or fields.Datetime.now()
                delta = relativedelta(end_data, rec.birthday)
                if delta.years <= 2:
                    age = str(delta.years) + _(" Year") + str(delta.months) + _(" Month ") + str(delta.days) + _(" Days")
                else:
                    age = str(delta.years) + _(" Year")
            rec.age = age

    code = fields.Char(string='Identification Code', default='/',
        help='Identifier provided by the Health Center.')
    gender = fields.Selection([
        ('male', 'Male'), 
        ('female', 'Female'), 
        ('other', 'Other')], string='Gender', required=True, default='male')
    birthday = fields.Date(string='Date of Birth')
    date_of_death = fields.Date(string='Date of Death')
    age = fields.Char(string='Age', compute='_get_age')
    is_referring_doctor = fields.Boolean(string="Is Referring Physician")
    hospital_name = fields.Char()
    blood_group = fields.Selection([
        ('A+', 'A+'),('A-', 'A-'),
        ('B+', 'B+'),('B-', 'B-'),
        ('AB+', 'AB+'),('AB-', 'AB-'),
        ('O+', 'O+'),('O-', 'O-')], string='Blood Group')


class ResUsers(models.Model):
    _inherit= "res.users"

    @api.depends('physician_ids')
    def _compute_physician_count(self):
        for user in self.with_context(active_test=False):
            user.physician_count = len(user.physician_ids)

    def _compute_patient_count(self):
        Patient = self.env['hms.patient']
        for user in self.with_context(active_test=False):
            user.patient_count = Patient.search_count([('partner_id','=', user.partner_id.id)])

    department_ids = fields.Many2many('hr.department', 'user_department_rel', 'user_id','department_id', 
        domain=[('patient_depatment', '=', True)], string='Departments')
    physician_count = fields.Integer(string="#Physician", compute="_compute_physician_count")
    physician_ids = fields.One2many('hms.physician', 'user_id', string='Related Physician')
    patient_count = fields.Integer(string="#Patient", compute="_compute_patient_count")

    def action_create_physician(self):
        self.ensure_one()
        self.env['hms.physician'].create({
            'user_id': self.id,
            'name': self.name,
        })

    def action_create_patient(self):
        self.ensure_one()
        self.env['hms.patient'].create({
            'partner_id': self.partner_id.id,
            'name': self.name,
        })


class HospitalDepartment(models.Model):
    _inherit = 'hr.department'

    note = fields.Text('Note')
    patient_depatment = fields.Boolean("Patient Department", default=True)


class ACSEthnicity(models.Model):
    _description = "Ethnicity"
    _name = 'acs.ethnicity'

    name = fields.Char(string='Name', required=True ,translate=True)
    code = fields.Char(string='Code')
    notes = fields.Char(string='Notes')

    _sql_constraints = [('name_uniq', 'UNIQUE(name)', 'Name must be unique!')]


class ACSMedicalAlert(models.Model):
    _name = 'acs.medical.alert'
    _description = "Medical Alert for Patient"

    name = fields.Char(required=True)
    description = fields.Text('Description')


class HrEmployeePublic(models.Model):
    _inherit = 'hr.employee.public'

    birthday = fields.Date('Date of Birth', tracking=True)