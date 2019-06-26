# __author__ = 'trananhdung'
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons import decimal_precision as dp


class MrpBOMLine(models.Model):
    _inherit = 'mrp.bom.line'

    @api.multi
    @api.depends('product_id.diameter')
    def _compute_diameter_code(self):
        for r in self:
            r.diameter_code = 'T%s' % int(r.product_id.diameter)

    @api.multi
    @api.depends('product_id.product_tmpl_id.inkg', 'spacing.p1', 'spacing.p2', 'spacing.p3',
                 'spacing.x', 'spacing.y', 'spacing.z', 'sketch.total_length', 'no_of_member')
    def _compute_totals(self):
        for r in self:
            r.bar_length = r.sketch.total_length
            # r.no_in_member = (r.spacing.x / r.spacing.p1 + r.spacing.y / r.spacing.p2 + r.spacing.z / r.spacing.p3) * 2
            r.total_length = r.no_in_member * r.bar_length * r.no_of_member / 1000
            r.total_weight = r.total_length * r.product_id.product_tmpl_id.inkg

    @api.multi
    @api.depends('input_product_qty', 'type', 'pvc_pipe_qty_ids.total_length',
                 'pc_strand_qty_ids.total_length', 'concrete_vol', 'total_weight')
    def _compute_product_qty(self):
        for r in self:
            if r.type == 'concrete':
                r.product_qty = r.concrete_vol
            elif r.type == 'pc_strand':
                r.product_qty = sum(r.pc_strand_qty_ids.mapped('total_length'))
            elif r.type == 'pvc_pipe':
                r.product_qty = sum(r.pvc_pipe_qty_ids.mapped('total_length'))
            elif r.type == 'rebar':
                r.product_qty = r.total_weight
            else:
                r.product_qty = r.input_product_qty

    @api.multi
    @api.depends('concrete_density', 'bom_id.product_id.csa', 'bom_id.product_tmpl_id.csa', 'bom_id.length')
    def _compute_concrete_vol(self):
        for r in self:
            r.concrete_vol = (r.bom_id.product_id.id and r.bom_id.product_id.csa or r.bom_id.product_tmpl_id.csa) * \
                             r.bom_id.length / 1000

    name = fields.Char(string=_('Name'))
    type = fields.Selection(selection=[('normal', _('Normal')),
                                       ('concrete', _('Concrete')),
                                       ('pc_strand', _('PC Strand')),
                                       ('pvc_pipe', _('PVC Pipe')),
                                       ('rebar', _('Rebar'))],
                            string=_('Type'), related='product_id.pretasi_type', readonly=True)
    product_qty = fields.Float(compute='_compute_product_qty')
    input_product_qty = fields.Float(
        'Quantity', default=1.0,
        digits=dp.get_precision('Product Unit of Measure'), required=True
    )

    pvc_pipe_qty_ids = fields.One2many(comodel_name='pvc_pipe.quantity', inverse_name='bom_line_id',
                                       string=_('PVC Quantities'), copy=True)
    pc_strand_qty_ids = fields.One2many(comodel_name='pc_strand.quantity',
                                        inverse_name='bom_line_id', string=_('PC Strand Quantites'), copy=True)

    # Concrete
    concrete_vol = fields.Float(string=_(u'Vol (m\u00b3)'), compute='_compute_concrete_vol', digits=(12, 3), store=True)
    concrete_density = fields.Float(string=_('Density'), default=1.0)

    # For Rebar
    diameter = fields.Float(related='product_id.diameter', store=True, readonly=True)
    diameter_code = fields.Char(string=_('Bar Diameter'), compute='_compute_diameter_code')
    bar_mark = fields.Float(string=_('Bar Mark'), digits=(12, 3))
    bar_length = fields.Float(string=_('Bar Length (mm)'), digits=(12, 0), compute='_compute_totals', store=True)
    member_length = fields.Float(string=_('Member Length (mm)'), digits=(12, 0),
                                 related='bom_id.length', store=True, readonly=True)
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
            self.no_in_member = self.spacing.length
