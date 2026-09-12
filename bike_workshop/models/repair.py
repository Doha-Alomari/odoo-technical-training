from odoo import api, models, fields
from odoo.exceptions import ValidationError
from .service_mixin import ServiceInfoMixin


class Repair(ServiceInfoMixin, models.Model):
    _name = 'bike.workshop.repair'
    _description = 'Bike Repair'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'bike.workshop.repair'
                ) or 'New'
        return super().create(vals_list)

    name = fields.Char(
        string='Repair Reference',
        required=True,
        readonly=True,
        copy=False,
        default='New',
    )

    customer_id = fields.Many2one(
        'res.partner',
        string='Customer',
        required=True,
    )

    bike_source = fields.Selection(
        [
            ('workshop', 'Workshop Bike'),
            ('external', 'External Bike'),
        ],
        string='Bike Source',
        required=True,
    )

    bike_id = fields.Many2one(
        'bike.workshop.bike',
        string='Workshop Bike',
    )

    external_reference = fields.Char(
        string='External Bike Reference',
    )

    external_brand = fields.Char(
        string='External Bike Brand',
    )

    external_bike_type = fields.Selection(
        [
            ('road', 'Road'),
            ('mountain', 'Mountain'),
            ('city', 'City'),
            ('electric', 'Electric'),
        ],
        string='External Bike Type',
    )

    reported_issue = fields.Text(
        string='Reported Issue',
        required=True,
    )

    total_parts_cost = fields.Float(
        string='Total Spare Parts Cost',
        compute='_compute_total_parts_cost',
        store=True,
    )

    part_line_ids = fields.One2many(
        'bike.workshop.repair.part.line',
        'repair_id',
        string='Spare Parts',
    )

    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='draft',
        required=True,
    )

    @api.depends('part_line_ids.subtotal')
    def _compute_total_parts_cost(self):
        for repair in self:
            repair.total_parts_cost = sum(
                repair.part_line_ids.mapped('subtotal')
            )

    @api.constrains(
        'bike_source',
        'bike_id',
        'external_reference',
        'external_brand',
        'external_bike_type',
    )
    def _check_bike_source(self):
        for repair in self:
            if repair.bike_source == 'workshop' and not repair.bike_id:
                raise ValidationError(
                    'Please select a Workshop Bike.'
                )

            if repair.bike_source == 'external':
                if not repair.external_reference:
                    raise ValidationError(
                        'Please enter the External Bike Reference.'
                    )

                if not repair.external_brand:
                    raise ValidationError(
                        'Please enter the External Bike Brand.'
                    )

                if not repair.external_bike_type:
                    raise ValidationError(
                        'Please select the External Bike Type.'
                    )

    def action_start(self):
        for repair in self:
            if repair.state != 'draft':
                raise ValidationError(
                    'Only Draft Repairs can be started.'
                )

            if not repair.customer_id:
                raise ValidationError(
                    'Customer is required to start the repair.'
                )

            if not repair.reported_issue:
                raise ValidationError(
                    'Reported Issue is required to start the repair.'
                )

            if not repair.assigned_mechanic:
                raise ValidationError(
                    'Assigned Mechanic is required to start the repair.'
                )

            repair.state = 'in_progress'

    def action_complete(self):
        for repair in self:
            if repair.state != 'in_progress':
                raise ValidationError(
                    'Only In Progress Repairs can be completed.'
                )

            if not repair.service_notes:
                raise ValidationError(
                    'Service Notes are required to complete the repair.'
                )

            if not repair.last_service_date:
                raise ValidationError(
                    'Last Service Date is required to complete the repair.'
                )

            repair.state = 'completed'

    def action_cancel(self):
        for repair in self:
            if repair.state not in ('draft', 'in_progress'):
                raise ValidationError(
                    'Only Draft or In Progress Repairs can be cancelled.'
                )

            repair.state = 'cancelled'


class RepairPartLine(models.Model):
    _name = 'bike.workshop.repair.part.line'
    _description = 'Repair Spare Part'

    repair_id = fields.Many2one(
        'bike.workshop.repair',
        string='Repair',
        required=True,
        ondelete='cascade',
    )

    product_id = fields.Many2one(
        'product.product',
        string='Product',
        required=True,
    )

    quantity = fields.Float(
        string='Quantity',
        required=True,
        default=1.0,
    )

    unit_price = fields.Float(
        string='Unit Price',
        required=True,
    )

    subtotal = fields.Float(
        string='Subtotal',
        compute='_compute_subtotal',
        store=True,
    )

    @api.depends('quantity', 'unit_price')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.unit_price

    @api.onchange('product_id')
    def _onchange_product(self):
        if self.product_id:
            self.unit_price = self.product_id.list_price

    @api.constrains('quantity', 'unit_price', 'subtotal')
    def _check_positive_values(self):
        for line in self:
            if line.quantity < 0:
                raise ValidationError(
                    'Quantity cannot be negative.'
                )

            if line.unit_price < 0:
                raise ValidationError(
                    'Unit Price cannot be negative.'
                )

            if line.subtotal < 0:
                raise ValidationError(
                    'Subtotal cannot be negative.'
                )