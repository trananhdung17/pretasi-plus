# __author__ = 'trananhdung'
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import odoo.addons.decimal_precision as dp


class PVCPipeQuantity(models.Model):
    _name = 'pvc_pipe.quantity'

    @api.multi
    @api.depends('length', 'no_in_member', 'no_of_member')
    def _compute_length(self):
        for r in self:
            r.total_length = r.length * r.no_in_member * r.no_of_member / 1000

    @api.model
    def _get_default_product(self):
        return self.env.ref('pretasi_mrp_boq.pretasi_product_product_pvc_pipe')

    product_id = fields.Many2one(comodel_name='product.product', readonly=True, required=True, default=_get_default_product)
    bom_line_id = fields.Many2one(comodel_name='mrp.bom.line', string=_('Bill of Quantity'))
    length = fields.Float(string=_('Length (mm)'), digits=(12, 0))
    no_in_member = fields.Float(string=_('No in Members'), digits=(12, 2))
    no_of_member = fields.Float(string=_('No of Members'), digits=(12, 2))
    total_length = fields.Float(string=_('Total Length (m)'), digits=(12, 3),
                                compute='_compute_length', store=True, readonly=True)
