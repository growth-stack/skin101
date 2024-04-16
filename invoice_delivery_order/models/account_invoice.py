from odoo import api, fields, models

class AccountMove(models.Model):
    _inherit = 'account.move'

    delivery_count = fields.Integer(string='Delivery Count', compute='_compute_delivery_count')
    delivery_ids = fields.One2many('stock.picking', 'move_id', string='Pickings')

    @api.depends('delivery_ids')
    def _compute_delivery_count(self):
        for move in self:
            move.delivery_count = len(move.delivery_ids)

    def action_post(self):
        StockPicking = self.env['stock.picking']
        for rec in self:
            for line in rec.invoice_line_ids:
                if line.product_id.detailed_type == 'product':
                    picking_vals = {
                        'move_id': rec.id,
                        'partner_id': line.partner_id.id,
                        'picking_type_id': self.env.ref('stock.picking_type_out').id,
                        'location_id': self.env.ref('stock.stock_location_stock').id,
                        'location_dest_id': self.env.ref('stock.stock_location_customers').id,
                        'move_type': 'direct'
                    }
                    picking = StockPicking.create(picking_vals)
                    move_vals = {
                    'name': line.name,
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.quantity,
                    'product_uom': line.product_uom_id.id,
                    'picking_id': picking.id,
                    'location_id': self.env.ref('stock.stock_location_stock').id,
                    'location_dest_id': self.env.ref('stock.stock_location_customers').id,
                    }
                    move = self.env['stock.move'].create(move_vals)

                    move._action_confirm()
                    move._action_assign()
                    move.move_line_ids.write({'qty_done': line.quantity})
            super(AccountMove, rec).action_post()

    def action_view_delivery(self):
        self.ensure_one()
        action = self.env.ref('stock.action_picking_tree_all').read()[0]
        action['views'] = [(self.env.ref('stock.view_picking_form').id, 'form')]
        action['res_id'] = self.delivery_ids[0].id if self.delivery_ids else False
        return action
