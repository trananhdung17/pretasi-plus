# __author__ = 'trananhdung'
# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.addons import decimal_precision as dp
from odoo.tools import float_round


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    product_qty = fields.Float(digits=dp.get_precision('Product Unit of Measure'))


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.depends('move_line_ids.qty_done', 'move_line_ids.product_uom_id', 'move_line_nosuggest_ids.qty_done')
    def _quantity_done_compute(self):
        """ This field represents the sum of the move lines `qty_done`. It allows the user to know
        if there is still work to do.

        We take care of rounding this value at the general decimal precision and not the rounding
        of the move's UOM to make sure this value is really close to the real sum, because this
        field will be used in `_action_done` in order to know if the move will need a backorder or
        an extra move.
        """
        for move in self:
            quantity_done = 0
            for move_line in move._get_move_lines():
                quantity_done += move_line.product_uom_id._compute_quantity(move_line.qty_done, move.product_uom,
                                                                            round=False)
            move.quantity_done = quantity_done
            pass

    quantity_done = fields.Float(compute='_quantity_done_compute', store=True,
                                 digits=dp.get_precision('Product Unit of Measure'))
