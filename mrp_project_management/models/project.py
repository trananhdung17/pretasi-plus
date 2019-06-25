# __author__ = 'trananhdung'
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ProjectProject(models.Model):
    _inherit = 'project.project'

    production_ids = fields.One2many(comodel_name='mrp.production', string=_('Manufacturing Orders'))
