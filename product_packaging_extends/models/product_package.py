# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.float_utils import float_round
from odoo.tools.float_utils import float_compare, float_is_zero, float_round


class ProductPackaging(models.Model):
    _inherit = 'product.packaging'

    cost_per_package = fields.Float(string="Cost per Package", compute='_compute_cost_per_package', store=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id, store=True)

    @api.depends('product_id', 'qty', 'product_id.standard_price')
    def _compute_cost_per_package(self):
        for product in self:
            product.cost_per_package = product.product_id.standard_price * product.qty
