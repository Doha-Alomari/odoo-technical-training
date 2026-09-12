from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_spare_part = fields.Boolean(
        string='Spare Part',
    )