# __author__ = 'trananhdung'
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class MRPProduction(models.Model):
    _inherit = 'mrp.production'

    boq_id = fields.Many2one(comodel_name='mrp.boq', string='BOQ')
