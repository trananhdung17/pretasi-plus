# # __author__ = 'trananhdung'
# # -*- coding: utf-8 -*-
#
# from odoo import models, fields, api, _
# from odoo.tools import float_compare, float_round, float_is_zero
# from odoo.exceptions import UserError
#
#
# class MRPProduction(models.Model):
#     _inherit = 'mrp.production'
#
#     use_boq = fields.Boolean(string=_('Use BOQ'), related='bom_id.boq')
#
#     def _prepare_move_raws_by_boq(self):
#         """
#
#         :return:
#         """
#         if self.routing_id:
#             routing = self.routing_id
#         else:
#             routing = self.bom_id.routing_id
#
#         if routing and routing.location_id:
#             source_location = routing.location_id
#         else:
#             source_location = self.location_src_id
#
#         original_quantity = (self.product_qty - self.qty_produced) or 1.0
#         result = []
#         sequence = 1
#         mo_route_id = self.env.ref('stock.route_warehouse0_mto')
#         product = self.bom_id.concrete_qty_ids.mapped('product_id')[0]
#         quantity = self.bom_id.total_concrete_vol * self.product_qty
#         concrete_vals = {
#             'sequence': sequence,
#             'name': self.name,
#             'date': self.date_planned_start,
#             'date_expected': self.date_planned_start,
#             # 'bom_line_id': bom_line.id,
#             'picking_type_id': self.picking_type_id.id,
#             'product_id': product.id,
#             'product_uom_qty': quantity,
#             'product_uom': product.uom_id.id,
#             'location_id': source_location.id,
#             'location_dest_id': product.property_stock_production.id,
#             'raw_material_production_id': self.id,
#             'company_id': self.company_id.id,
#             # 'operation_id': bom_line.operation_id.id or alt_op,
#             'price_unit': product.standard_price,
#             'procure_method': 'make_to_order' if mo_route_id.id in product.route_ids.ids else 'make_to_stock',
#             'origin': self.name,
#             'warehouse_id': source_location.get_warehouse().id,
#             'group_id': self.procurement_group_id.id,
#             'propagate': self.propagate,
#             'unit_factor': quantity / original_quantity,
#         }
#         result.append(concrete_vals)
#         product = self.bom_id.pvc_pipe_qty_ids.mapped('product_id')[0]
#         quantity = self.bom_id.total_pvc_pipe_length * self.product_qty
#         pvc_pipe_vals = {
#
#             'sequence': sequence,
#             'name': self.name,
#             'date': self.date_planned_start,
#             'date_expected': self.date_planned_start,
#             # 'bom_line_id': bom_line.id,
#             'picking_type_id': self.picking_type_id.id,
#             'product_id': product.id,
#             'product_uom_qty': quantity,
#             'product_uom': product.uom_id.id,
#             'location_id': source_location.id,
#             'location_dest_id': product.property_stock_production.id,
#             'raw_material_production_id': self.id,
#             'company_id': self.company_id.id,
#             # 'operation_id': bom_line.operation_id.id or alt_op,
#             'price_unit': product.standard_price,
#             'procure_method': 'make_to_order' if mo_route_id.id in product.route_ids.ids else 'make_to_stock',
#             'origin': self.name,
#             'warehouse_id': source_location.get_warehouse().id,
#             'group_id': self.procurement_group_id.id,
#             'propagate': self.propagate,
#             'unit_factor': quantity / original_quantity,
#         }
#         result.append(pvc_pipe_vals)
#         product = self.bom_id.pc_strand_qty_ids.mapped('product_id')[0]
#         quantity = self.bom_id.total_pvc_pipe_length * self.product_qty
#         pc_strand_vals = {
#             'sequence': sequence,
#             'name': self.name,
#             'date': self.date_planned_start,
#             'date_expected': self.date_planned_start,
#             # 'bom_line_id': bom_line.id,
#             'picking_type_id': self.picking_type_id.id,
#             'product_id': product.id,
#             'product_uom_qty': quantity,
#             'product_uom': product.uom_id.id,
#             'location_id': source_location.id,
#             'location_dest_id': product.property_stock_production.id,
#             'raw_material_production_id': self.id,
#             'company_id': self.company_id.id,
#             # 'operation_id': bom_line.operation_id.id or alt_op,
#             'price_unit': product.standard_price,
#             'procure_method': 'make_to_order' if mo_route_id.id in product.route_ids.ids else 'make_to_stock',
#             'origin': self.name,
#             'warehouse_id': source_location.get_warehouse().id,
#             'group_id': self.procurement_group_id.id,
#             'propagate': self.propagate,
#             'unit_factor': quantity / original_quantity,
#         }
#         result.append(pc_strand_vals)
#         for rebar in self.bom_id.rebar_qty_ids:
#             # quantity = rebar.total_length
#             quantity = rebar.total_weight
#             rebar_vals = {
#                 'sequence': sequence,
#                 'product_id': rebar.product_id.id,
#                 'product_uom_qty': quantity,
#                 'product_uom': rebar.product_id.uom_id.id,
#                 'name': self.name,
#                 'date': self.date_planned_start,
#                 'date_expected': self.date_planned_start,
#                 # 'bom_line_id': bom_line.id,
#                 'picking_type_id': self.picking_type_id.id,
#                 'location_id': source_location.id,
#                 'location_dest_id': rebar.product_id.property_stock_production.id,
#                 'raw_material_production_id': self.id,
#                 'company_id': self.company_id.id,
#                 # 'operation_id': bom_line.operation_id.id or alt_op,
#                 'price_unit': rebar.product_id.standard_price,
#                 'procure_method': 'make_to_order' if mo_route_id.id in rebar.product_id.route_ids.ids else 'make_to_stock',
#                 'origin': self.name,
#                 'warehouse_id': source_location.get_warehouse().id,
#                 'group_id': self.procurement_group_id.id,
#                 'propagate': self.propagate,
#                 'unit_factor': quantity / original_quantity,
#             }
#             result.append(rebar_vals)
#         return result
#
#     def _generate_move_raw_lines_by_boq(self):
#         """
#
#         :return:
#         """
#         StockMove = self.env['stock.move']
#         for vals in self._prepare_move_raws_by_boq():
#             raw = StockMove.create(vals)
#             raw._action_confirm()
#
#     def generate_mo_lines_by_boq(self):
#         """
#
#         :return:
#         """
#         self.ensure_one()
#         if self.use_boq:
#             # self._generate_finished_line_by_boq()
#             self._generate_finished_moves()
#             self._generate_move_raw_lines_by_boq()
#         return
#
#     def _generate_moves(self):
#         if self.use_boq:
#             return True
#         else:
#             return super(MRPProduction, self)._generate_moves()
#
#     @api.model
#     def create(self, vals_list):
#         mo = super(MRPProduction, self).create(vals_list)
#         mo.generate_mo_lines_by_boq()
#         return mo
#
#
# class MrpProductProduce(models.TransientModel):
#     _inherit = "mrp.product.produce"
#
#     @api.onchange('product_qty')
#     def _onchange_product_qty(self):
#         lines = []
#         qty_todo = self.product_uom_id._compute_quantity(self.product_qty, self.production_id.product_uom_id, round=False)
#         for move in self.production_id.move_raw_ids.filtered(lambda m: m.state not in ('done', 'cancel')):
#             qty_to_consume = float_round(qty_todo * move.unit_factor, precision_rounding=move.product_uom.rounding)
#             for move_line in move.move_line_ids:
#                 if float_compare(qty_to_consume, 0.0, precision_rounding=move.product_uom.rounding) <= 0:
#                     break
#                 if move_line.lot_produced_id or float_compare(move_line.product_uom_qty, move_line.qty_done, precision_rounding=move.product_uom.rounding) <= 0:
#                     continue
#                 to_consume_in_line = min(qty_to_consume, move_line.product_uom_qty)
#                 lines.append({
#                     'move_id': move.id,
#                     'qty_to_consume': to_consume_in_line,
#                     'qty_done': to_consume_in_line,
#                     'lot_id': move_line.lot_id.id,
#                     'product_uom_id': move.product_uom.id,
#                     'product_id': move.product_id.id,
#                     'qty_reserved': min(to_consume_in_line, move_line.product_uom_qty),
#                 })
#                 qty_to_consume -= to_consume_in_line
#             if float_compare(qty_to_consume, 0.0, precision_rounding=move.product_uom.rounding) > 0:
#                 if move.product_id.tracking == 'serial':
#                     while float_compare(qty_to_consume, 0.0, precision_rounding=move.product_uom.rounding) > 0:
#                         lines.append({
#                             'move_id': move.id,
#                             'qty_to_consume': 1,
#                             'qty_done': 1,
#                             'product_uom_id': move.product_uom.id,
#                             'product_id': move.product_id.id,
#                         })
#                         qty_to_consume -= 1
#                 else:
#                     lines.append({
#                         'move_id': move.id,
#                         'qty_to_consume': qty_to_consume,
#                         'qty_done': qty_to_consume,
#                         'product_uom_id': move.product_uom.id,
#                         'product_id': move.product_id.id,
#                     })
#
#         self.produce_line_ids = [(5,)] + [(0, 0, x) for x in lines]
#
#
# class ChangeProductionQty(models.TransientModel):
#     _inherit = 'change.production.qty'
#
#     @api.multi
#     def change_prod_qty(self):
#         precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
#         wizard = self
#         production = wizard.mo_id
#         if not production.use_boq:
#             return super(ChangeProductionQty, self).change_prod_qty()
#
#         produced = sum(production.move_finished_ids.filtered(lambda m: m.product_id == production.product_id).mapped('quantity_done'))
#
#         if wizard.product_qty < produced:
#             format_qty = '%.{precision}f'.format(precision=precision)
#             raise UserError(_("You have already processed %s. Please input a quantity higher than %s ") % (format_qty % produced, format_qty % produced))
#
#         if production.state not in ('confirmed',):
#             raise UserError('You cannot update MO Quantity after started to produce')
#
#         production.write({'product_qty': wizard.product_qty})
#         production.move_finished_ids._action_cancel()
#         production.move_finished_ids.unlink()
#         production.move_raw_ids._action_cancel()
#         production.move_raw_ids.unlink()
#         production.generate_mo_lines_by_boq()
#
#         return {}
