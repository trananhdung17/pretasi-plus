# __author__ = 'trananhdung'
# -*- coding: utf-8 -*-

from odoo import fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    width = fields.Float(string=_('Width'))
    depth = fields.Float(string=_('Depth'))
    csa = fields.Float(string=_(u'Cross Sectional Area (m\u00b2)'))
    diameter = fields.Float(string=_('Diameter (mm)'))
    inkg = fields.Float(string=_('In Kg'))
