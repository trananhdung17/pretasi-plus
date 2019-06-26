# __author__ = 'trananhdung'
# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.addons import decimal_precision as dp


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    product_qty = fields.Float(digits=dp.get_precision('Product Unit of Measure'))
