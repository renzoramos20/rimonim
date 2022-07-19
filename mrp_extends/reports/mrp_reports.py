# -*- coding: utf-8 -*-

import json

from odoo import api, models, _
from odoo.tools import float_round

class ReportBomStructure(models.AbstractModel):
    _inherit = 'report.mrp.report_bom_structure'

    def _get_bom_lines(self, bom, bom_quantity, product, line_id, level):
        components = []
        total = 0
        for line in bom.bom_line_ids:
            line_quantity = (bom_quantity / (bom.product_qty or 1.0)) * line.product_qty
            if line._skip_bom_line(product):
                continue
            company = bom.company_id or self.env.company
            price = line.product_id.uom_id._compute_price(line.product_id.with_company(company).standard_price,
                                                          line.product_uom_id) * line_quantity
            if line.child_bom_id:
                factor = line.product_uom_id._compute_quantity(line_quantity, line.child_bom_id.product_uom_id)
                sub_total = self._get_price(line.child_bom_id, factor, line.product_id)
                byproduct_cost_share = sum(line.child_bom_id.byproduct_ids.mapped('cost_share'))
                if byproduct_cost_share:
                    sub_total *= float_round(1 - byproduct_cost_share / 100, precision_rounding=0.0001)
            else:
                sub_total = price
            sub_total = self.env.company.currency_id.round(sub_total)
            components.append({
                'prod_id': line.product_id.id,
                'prod_name': line.product_id.display_name,
                'code': line.child_bom_id and line.child_bom_id.display_name or '',
                'prod_qty': line_quantity,
                'decrease_percent': line.decrease_percent,
                'quantity_amount': line.quantity_amount,
                'prod_uom': line.product_uom_id.name,
                'prod_cost': company.currency_id.round(price),
                'parent_id': bom.id,
                'line_id': line.id,
                'level': level or 0,
                'total': sub_total,
                'child_bom': line.child_bom_id.id,
                'phantom_bom': line.child_bom_id and line.child_bom_id.type == 'phantom' or False,
                'attachments': self.env['mrp.document'].search(['|', '&',
                                                                ('res_model', '=', 'product.product'),
                                                                ('res_id', '=', line.product_id.id), '&',
                                                                ('res_model', '=', 'product.template'),
                                                                ('res_id', '=', line.product_id.product_tmpl_id.id)]),

            })
            total += sub_total
        return components, total

    def _get_sub_lines(self, bom, product_id, line_qty, line_id, level, child_bom_ids, unfolded):
        data = self._get_bom(bom_id=bom.id, product_id=product_id, line_qty=line_qty, line_id=line_id, level=level)
        bom_lines = data['components']
        lines = []
        for bom_line in bom_lines:
            lines.append({
                'name': bom_line['prod_name'],
                'type': 'bom',
                'quantity': bom_line['prod_qty'],
                'decrease_percent': bom_line['decrease_percent'],
                'quantity_amount': bom_line['quantity_amount'],
                'uom': bom_line['prod_uom'],
                'prod_cost': bom_line['prod_cost'],
                'bom_cost': bom_line['total'],
                'level': bom_line['level'],
                'code': bom_line['code'],
                'child_bom': bom_line['child_bom'],
                'prod_id': bom_line['prod_id']
            })
            if bom_line['child_bom'] and (unfolded or bom_line['child_bom'] in child_bom_ids):
                line = self.env['mrp.bom.line'].browse(bom_line['line_id'])
                lines += (self._get_sub_lines(line.child_bom_id, line.product_id.id, bom_line['prod_qty'], line, level + 1, child_bom_ids, unfolded))
        if data['operations']:
            lines.append({
                'name': _('Operations'),
                'type': 'operation',
                'quantity': data['operations_time'],
                'uom': _('minutes'),
                'bom_cost': data['operations_cost'],
                'level': level,
            })
            for operation in data['operations']:
                if unfolded or 'operation-' + str(bom.id) in child_bom_ids:
                    lines.append({
                        'name': operation['name'],
                        'type': 'operation',
                        'quantity': operation['duration_expected'],
                        'uom': _('minutes'),
                        'bom_cost': operation['total'],
                        'level': level + 1,
                    })
        if data['byproducts']:
                lines.append({
                    'name': _('Byproducts'),
                    'type': 'byproduct',
                    'uom': False,
                    'quantity': data['byproducts_total'],
                    'bom_cost': data['byproducts_cost'],
                    'level': level,
                })
                for byproduct in data['byproducts']:
                    if unfolded or 'byproduct-' + str(bom.id) in child_bom_ids:
                        lines.append({
                            'name': byproduct['product_name'],
                            'type': 'byproduct',
                            'quantity': byproduct['product_qty'],
                            'uom': byproduct['product_uom'],
                            'prod_cost': byproduct['product_cost'],
                            'bom_cost': byproduct['bom_cost'],
                            'level': level + 1,
                        })
        return lines