# __author__ = 'trananhdung'
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class MRPProduction(models.Model):
    _inherit = 'mrp.production'

    boq_id = fields.Many2one(comodel_name='mrp.boq', string='BOQ')
    use_boq = fields.Boolean(string=_('Use BOQ'), default=False)

    @api.onchange('boq_id')
    def onchange_boq(self):
        if self.boq_id:
            self.product_id = self.boq_id.product_id

    def _prepare_move_raws_by_boq(self):
        """

        :return:
        """
        if self.routing_id:
            routing = self.routing_id
        else:
            routing = self.boq_id.routing_id

        if routing and routing.location_id:
            source_location = routing.location_id
        else:
            source_location = self.location_src_id

        # original_quantity = (self.product_qty - self.qty_produced) or 1.0
        result = []
        sequence = 1
        product = self.concrete_qty_ids.mapped('product_id')[0]
        concrete_vals = {
            'sequence': sequence,
            'name': self.name,
            'date': self.date_planned_start,
            'date_expected': self.date_planned_start,
            # 'bom_line_id': bom_line.id,
            'picking_type_id': self.picking_type_id.id,
            'product_id': product.id,
            'product_uom_qty': self.total_concrete_vol * self.product_qty,
            'product_uom': product.uom_id.id,
            'location_id': source_location.id,
            'location_dest_id': product.property_stock_production.id,
            'raw_material_production_id': self.id,
            'company_id': self.company_id.id,
            # 'operation_id': bom_line.operation_id.id or alt_op,
            'price_unit': product.standard_price,
            'procure_method': 'make_to_stock',
            'origin': self.name,
            'warehouse_id': source_location.get_warehouse().id,
            'group_id': self.procurement_group_id.id,
            'propagate': self.propagate,
            # 'unit_factor': ,
        }
        result.append(concrete_vals)
        product = self.pvc_pipe_qty_ids.mapped('product_id')[0]
        pvc_pipe_vals = {

            'sequence': sequence,
            'name': self.name,
            'date': self.date_planned_start,
            'date_expected': self.date_planned_start,
            # 'bom_line_id': bom_line.id,
            'picking_type_id': self.picking_type_id.id,
            'product_id': product.id,
            'product_uom_qty': self.boq_id.total_pvc_pipe_length * self.product_qty,
            'product_uom': product.uom_id.id,
            'location_id': source_location.id,
            'location_dest_id': product.property_stock_production.id,
            'raw_material_production_id': self.id,
            'company_id': self.company_id.id,
            # 'operation_id': bom_line.operation_id.id or alt_op,
            'price_unit': product.standard_price,
            'procure_method': 'make_to_stock',
            'origin': self.name,
            'warehouse_id': source_location.get_warehouse().id,
            'group_id': self.procurement_group_id.id,
            'propagate': self.propagate,
            # 'unit_factor': ,
        }
        result.append(pvc_pipe_vals)
        product = self.pv_strand_qty_ids.mapped('product_id')[0]
        pc_strand_vals = {
            'sequence': sequence,
            'name': self.name,
            'date': self.date_planned_start,
            'date_expected': self.date_planned_start,
            # 'bom_line_id': bom_line.id,
            'picking_type_id': self.picking_type_id.id,
            'product_id': product.id,
            'product_uom_qty': self.boq_id.total_pvc_pipe_length * self.product_qty,
            'product_uom': product.uom_id.id,
            'location_id': source_location.id,
            'location_dest_id': product.property_stock_production.id,
            'raw_material_production_id': self.id,
            'company_id': self.company_id.id,
            # 'operation_id': bom_line.operation_id.id or alt_op,
            'price_unit': product.standard_price,
            'procure_method': 'make_to_stock',
            'origin': self.name,
            'warehouse_id': source_location.get_warehouse().id,
            'group_id': self.procurement_group_id.id,
            'propagate': self.propagate,
        }
        result.append(pc_strand_vals)
        for rebar in self.rebar_qty_ids:

            rebar_vals = {
                'sequence': sequence,
                'product_id': rebar.product_id.id,
                'product_uom_qty': rebar.total_length,
                'product_uom': rebar.product_id.uom_id,
                'name': self.name,
                'date': self.date_planned_start,
                'date_expected': self.date_planned_start,
                # 'bom_line_id': bom_line.id,
                'picking_type_id': self.picking_type_id.id,
                'location_id': source_location.id,
                'location_dest_id': rebar.product_id.property_stock_production.id,
                'raw_material_production_id': self.id,
                'company_id': self.company_id.id,
                # 'operation_id': bom_line.operation_id.id or alt_op,
                'price_unit': rebar.product_id.standard_price,
                'procure_method': 'make_to_stock',
                'origin': self.name,
                'warehouse_id': source_location.get_warehouse().id,
                'group_id': self.procurement_group_id.id,
                'propagate': self.propagate,
            }
            result.append(rebar_vals)
        return result

    def _generate_move_raw_lines_by_boq(self):
        """

        :return:
        """
        StockMove = self.env['stock.move']
        for vals in self._prepare_move_raws_by_boq():
            raw = StockMove.create(vals)
            raw.action_confirm()

    def generate_mo_lines_by_boq(self):
        """

        :return:
        """
        self.ensure_one()
        if self.use_boq and self.boq_id.id:
            self._generate_finished_line_by_boq()
            # self._generate_finished_moves()
        return

    @api.model
    def create(self, vals_list):
        mo = super(MRPProduction, self).create(vals_list)
        mo.generate_mo_lines_by_boq()
        return mo
