# __author__ = 'trananhdung'
# -*- coding: utf-8 -*-

from odoo import fields, api, models, _


class ProjectPrject(models.Model):
    _inherit = 'project.project'

    @api.multi
    @api.depends('boq_ids')
    def _compute_count_boq(self):
        for r in self:
            r.boq_count = len(r.boq_ids)

    boq_ids = fields.One2many(comodel_name='mrp.boq', string='BOQs', inverse_name='project_id')
    boq_count = fields.Integer(compute='_compute_count_boq', string=_('BOQ Count'), readonly=1, store=True)

    @api.multi
    def action_create_boq(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'mrp.boq',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current',
            'res_id': False,
            'context': {'default_project_id': self.id},
            'name': _('Create Bill of Quantity')
        }

    @api.multi
    def action_open_boq(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Bill of Quantity'),
            'res_model': 'mrp.boq',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'target': 'current',
            'domain': [('id', 'in', self.boq_ids.ids)],
            'context': {'default_project_id': self.id}
        }
