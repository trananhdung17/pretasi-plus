# __author__ = 'trananhdung'
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class MrpBOQLine(models.Model):
    _name = 'rebar.quantity'

    @api.multi
    @api.depends('product_id.diameter')
    def _compute_diameter_code(self):
        for r in self:
            r.diameter_code = 'T%s' % r.product_id.diameter

    @api.multi
    @api.depends('product_id.product_tmpl_id.inkg', 'spacing.p1', 'spacing.p2', 'spacing.p3',
                 'spacing.x', 'spacing.y', 'spacing.z', 'sketch.total_length', 'no_of_member')
    def _compute_totals(self):
        for r in self:
            r.bar_length = r.sketch.total_length
            # r.no_in_member = (r.spacing.x / r.spacing.p1 + r.spacing.y / r.spacing.p2 + r.spacing.z / r.spacing.p3) * 2
            r.total_length = r.no_in_member * r.bar_length * r.no_of_member / 1000
            r.total_weight = r.total_weight * r.product_id.product_tmpl_id.inkg

    boq_id = fields.Many2one(comodel_name='mrp.boq', string='BOQ')
    product_id = fields.Many2one(string=_('Product'), comodel_name='product.product')
    diameter = fields.Float(related='product_id.diameter', store=True, readonly=True)
    diameter_code = fields.Char(string=_('Bar Diameter'), compute='_compute_diameter_code')
    bar_mark = fields.Float(string=_('Bar Mark'), digits=(12, 3))
    bar_length = fields.Float(string=_('Bar Length (mm)'), digits=(12, 0), compute='_compute_totals', store=True)
    member_length = fields.Float(string=_('Member Length (mm)'), digits=(12, 0))
    spacing = fields.Many2one(comodel_name='rebar.quantity.spacing', string=_('Spacing (mm)'))
    no_in_member = fields.Float(string=_('No in Members'), digits=(12, 3),
                                # compute='_compute_totals', store=True
                                )
    no_of_member = fields.Float(string=_('No of Members'), digits=(12, 3))
    total_length = fields.Float(string=_('Total Length (m)'), compute='_compute_totals', digits=(12, 3), store=True)
    total_weight = fields.Float(string=_('Total Weight (Kg)'), compute='_compute_totals', digits=(12, 3), store=True)
    sketch = fields.Many2one(comodel_name='rebar.quantity.sketch', string=_('Sketch'))

    @api.onchange('spacing')
    def onchange_spacing(self):
        if self.spacing:
            self.no_in_member = (self.spacing.x / self.spacing.p1 + self.spacing.y / self.spacing.p2 + self.spacing.z / self.spacing.p3) * 2


class RebarSpacing(models.Model):
    _name = 'rebar.quantity.spacing'

    @api.multi
    @api.depends('p1', 'p2', 'p3')
    def _compute_display_name(self):
        for r in self:
            r.display_name = '\n'.join([str(c) for c in [r.p1, r.p2, r.p3] if c])

    display_name = fields.Text(string=_('Name'), compute='_compute_display_name', store=True)
    p1 = fields.Float(string=_('Space 1'), digits=(12, 0))
    p2 = fields.Float(string=_('Space 2'), digits=(12, 0))
    p3 = fields.Float(string=_('Space 3'), digits=(12, 0))
    x = fields.Float(string=_('X'), digits=(12, 0))
    y = fields.Float(string=_('Y'), digits=(12, 0))
    z = fields.Float(string=_('Z'), digits=(12, 0))

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        return []

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        return []


class RebarSketch(models.Model):
    _name = 'rebar.quantity.sketch'

    @api.multi
    @api.depends('line_ids.value', 'line_ids.name')
    def _compute_info(self):
        for r in self:
            r.total_length = sum(r.line_ids.mapped('value'))
            r.display_name = '\n'.join(['{name}: {value}'.format(name=line.name, value=line.value) for line in r.line_ids])

    display_name = fields.Text(string=_('Name'), compute='_compute_info')
    line_ids = fields.One2many(comodel_name='rebar.quantity.sketch.line', inverse_name='sketch_id')
    total_length = fields.Float(string=_('Length (mm)'), compute='_compute_info', store=True)

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        return []

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        return []

class RebarSketchLine(models.Model):
    _name = 'rebar.quantity.sketch.line'

    sketch_id = fields.Many2one(comodel_name='rebar.quantity.sketch')
    name = fields.Char(string=_('Name'), required=True)
    value = fields.Float(string=_('Length (mm)'), digits=(12, 0), required=True)
