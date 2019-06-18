# __author__ = 'trananhdung'
# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class ConcreteQuantity(models.Model):
    _name = 'concrete.quantity'

    @api.multi
    @api.depends('product_id.csa', 'boq_id.quantity')
    def _compute_vol(self):
        for r in self:
            r.vol = r.product_id.csa * r.boq_id.quantity

    boq_id = fields.Many2one(comodel_name='mrp.boq', string='BOQ')
    product_id = fields.Many2one(string='Product', comodel_name='product.product', required=True)
    vol = fields.Float(string=_('Total Vol'), compute='_compute_vol', store=True)
    density = fields.Float(string=_('Concrete Density'))
