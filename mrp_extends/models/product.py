# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.float_utils import float_round
from odoo.tools.float_utils import float_compare, float_is_zero, float_round

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    standard_price = fields.Float(
        'Cost', compute='_compute_standard_price',
        inverse='_set_standard_price', search='_search_standard_price',
        digits=(16, 5), groups="base.group_user",
        help="""In Standard Price & AVCO: value of the product (automatically computed in AVCO).
           In FIFO: value of the next unit that will leave the stock (automatically computed).
           Used to value the product when the purchase cost is not known (e.g. inventory adjustment).
           Used to compute margins on sale orders.""")

class ProductProduct(models.Model):
    _inherit = 'product.product'

    standard_price = fields.Float(
            'Cost', company_dependent=True,
            digits=(16, 5),
            groups="base.group_user",
            help="""In Standard Price & AVCO: value of the product (automatically computed in AVCO).
            In FIFO: value of the next unit that will leave the stock (automatically computed).
            Used to value the product when the purchase cost is not known (e.g. inventory adjustment).
            Used to compute margins on sale orders.""")