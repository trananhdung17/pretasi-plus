# __author__ = 'trananhdung'
# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class ConcreteQuantity(models.Model):
    _name = 'concrete.quantity'

    @api.multi
    @api.depends('boq_id.product_id.csa', 'boq_id.quantity', 'density')
    def _compute_vol(self):
        for r in self:
            r.vol = r.boq_id.product_id.csa * r.boq_id.quantity * r.density / 1000

    boq_id = fields.Many2one(comodel_name='mrp.boq', string='BOQ')
    product_id = fields.Many2one(string=_('Product'), comodel_name='product.product', required=True)
    density = fields.Float(string=_('Concrete Density'), default=1.0)
    vol = fields.Float(string=_(u'Total Vol (m\u00b3)'), compute='_compute_vol', store=True)
