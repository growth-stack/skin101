from odoo import models, fields, api, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    move_id = fields.Many2one('account.move', string='Account Move')
