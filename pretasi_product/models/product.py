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

    pretasi_type = fields.Selection(selection=[('normal', _('Normal')),
                                               ('concrete', _('Concrete')),
                                               ('pc_strand', _('PC Strand')),
                                               ('pvc_pipe', _('PVC Pipe')),
                                               ('rebar', _('Rebar'))],
                                    default='normal', string=_('Type'))
