# __author__ = 'trananhdung'
# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class MRPBOQ(models.Model):
    _inherit = 'mrp.boq'

    project_id = fields.Many2one(comodel_name='project.project', string=_('Project'),
                                 readonly=True, states={'draft': [('readonly', False)]})
