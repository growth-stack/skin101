from odoo import fields,api,models,_

class ResPartner(models.Model):
    _inherit = 'res.partner'

    signature_count = fields.Integer()