# __author__ = 'trananhdung'
# -*- coding: utf-8 -*-

from odoo import models, api, fields, _


class MrpBOQ(models.Model):
    _inherit = ['mail.thread']
    _name = 'mrp.boq'
    _description = 'Bill of Quantity for Beam'

    name = fields.Char(string=_('Name'), required=True, readonly=True, states={'draft': [('readonly', False)]})
    state = fields.Selection(string=_('Status'), selection=[('draft', _('Draft')),
                                                            ('confirmed', _('Confirmed')),
                                                            ('cancelled', _('Cancelled'))], default='draft',
                             track_visibility='always')
    quantity = fields.Float(string=_('Length (m)'), digits=(12, 3), required=True,
                            readonly=True, states={'draft': [('readonly', False)]})
    product_id = fields.Many2one(comodel_name='product.product', string=_('Beam'), required=True,
                                 readonly=True, states={'draft': [('readonly', False)]})
    product_uom_id = fields.Many2one(comodel_name='uom.uom', string=_('UoM'), required=True,
                                     readonly=True, states={'draft': [('readonly', False)]})
    cast = fields.Char(string=_('Key in Cast'), readonly=True, states={'draft': [('readonly', False)]})

    pvc_pipe_qty_ids = fields.One2many(comodel_name='pvc_pipe.quantity',
                                       inverse_name='boq_id', string=_('PVC Quantities'),
                                       readonly=True, states={'draft': [('readonly', False)]})
    pc_strand_qty_ids = fields.One2many(comodel_name='pc_strand.quantity',
                                        inverse_name='boq_id', string=_('PC Strand Quantites'),
                                        readonly=True, states={'draft': [('readonly', False)]})
    rebar_qty_ids = fields.One2many(comodel_name='rebar.quantity', inverse_name='boq_id', string=_('Rebar Quantities'),
                                    readonly=True, states={'draft': [('readonly', False)]})
    concrete_qty_ids = fields.One2many(comodel_name='concrete.quantity', inverse_name='boq_id',
                                       string=_('Concrete Quantities'),
                                       readonly=True, states={'draft': [('readonly', False)]})
    production_ids = fields.One2many(comodel_name='mrp.production', inverse_name='boq_id')
    production_count = fields.Integer(string=_('Production Count'))

    def _open_manufacturing_orders(self):
        """

        :return:
        """
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': self.production_ids.ids[0],
            'target': 'current',
            'name': 'Manufacturing Order'
        }

    @api.multi
    def action_confirm(self):
        return self.write({'state': 'confirmed'})

    @api.multi
    def action_cancel(self):
        return self.write({'state': 'cancelled'})

    @api.multi
    def action_set_to_draft(self):
        return self.write({'state': 'draft'})

    def _prepare_mo_vals(self):
        """

        :return:
        """
        vals = {

        }
        return vals

    @api.multi
    def action_create_or_open_mo(self):
        """

        :return:
        """
        self.ensure_one()
        if not self.production_ids.ids:
            mo_vals = self._prepare_mo_vals()
            self.env['mrp.production'].create(mo_vals)
        return self._open_manufacturing_orders()
