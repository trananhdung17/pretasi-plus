# __author__ = 'trananhdung'
# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class ConcreteQuantity(models.Model):
    _name = 'concrete.quantity'

    @api.multi
    @api.depends('bom_id.product_id.csa', 'bom_id.length', 'density', 'bom_id.product_qty')
    def _compute_vol(self):
        for r in self:
            r.vol = r.boq_id.product_id.csa * r.bom_id.length * r.bom_id.product_qty * r.density / 1000

    bom_id = fields.Many2one(comodel_name='mrp.bom', string='BOQ')
    product_id = fields.Many2one(string=_('Product'), comodel_name='product.product', required=True)
    density = fields.Float(string=_('Concrete Density'), default=1.0)
    vol = fields.Float(string=_(u'Total Vol (m\u00b3)'), compute='_compute_vol', store=True)
