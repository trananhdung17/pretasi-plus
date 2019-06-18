# __author__ = 'trananhdung'
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import odoo.addons.decimal_precision as dp


class PCStrandQuantity(models.Model):
    _name = 'pc_strand.quantity'

    @api.multi
    @api.depends('length', 'no_in_member', 'total_cast')
    def _compute_length(self):
        for r in self:
            r.total_length = r.length * r.no_in_member * r.total_cast
            r.total_weight = r.total_length * 1.12

    @api.model
    def _get_default_product(self):
        return self.env.ref('pretasi_mrp_boq.pretasi_product_pc_strand')

    product_id = fields.Many2one(comodel_name='product.product', readonly=True, required=True, default=_get_default_product)
    boq_id = fields.Many2one(comodel_name='mrp.boq', string=_('Bill of Quantity'))
    length = fields.Float(string=_('Length (m)'), digits=(12, 3))
    no_in_member = fields.Float(string=_('No in Members'), digits=(12, 2))
    bed_line = fields.Float(string=_('Bed Line'), digits=(12, 2))
    total_cast = fields.Float(string=_('Total Cast'), digits=(12, 2))
    total_length = fields.Float(string=_('Total Length (m)'), digits=(12, 3),
                                compute='_compute_length', store=True, readonly=True)
    total_weight = fields.Float(string=_('Total Weight (Kg)'), digits=(12, 3), compute='_compute_length')
