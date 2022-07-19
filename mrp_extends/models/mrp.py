# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.float_utils import float_round
from odoo.tools.float_utils import float_compare, float_is_zero, float_round

class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    @api.onchange('bom_line_ids')
    def _compute_product_qty(self):
        for bom in self:
            for line in bom.bom_line_ids:
                percent = (line.quantity_amount * line.decrease_percent) / 100
                line.product_qty = line.quantity_amount - percent


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    quantity_amount = fields.Float(string="Quantity", default=1.0,)
    decrease_percent = fields.Float(string="Decrease %")
    product_qty = fields.Float(
        'Quantity', digits='Product Unit of Measure', required=True, store=True)
