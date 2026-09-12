from odoo import api, models, fields
from odoo.exceptions import ValidationError


class Rental(models.Model):
    _name = 'bike.workshop.rental'
    _description = 'Bike Rental'

    name = fields.Char(
        string='Rental Reference',
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

    bike_id = fields.Many2one(
        'bike.workshop.bike',
        string='Bike',
        required=True,
    )

    start_date = fields.Date(
        string='Rental Start Date',
        required=True,
    )

    expected_return_date = fields.Date(
        string='Expected Return Date',
        required=True,
    )

    actual_return_date = fields.Date(
        string='Actual Return Date',
         readonly=True,
    )

    daily_price = fields.Float(
        string='Daily Rental Price',
        required=True,
    )

    duration = fields.Integer(
        string='Rental Duration (Days)',
        compute='_compute_duration',
        store=True,
    )

    total_amount = fields.Float(
        string='Total Rental Amount',
        compute='_compute_total_amount',
        store=True,
    )

    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('returned', 'Returned'),
        ],
        string='Status',
        default='draft',
        required=True,
        readonly=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'bike.workshop.rental'
                ) or 'New'
        return super().create(vals_list)

    def action_confirm(self):
        for rental in self:
            if rental.state != 'draft':
                raise ValidationError(
                    'Only Draft Rentals can be confirmed.'
                )
            conflicting_rental = self.search([
                ('id', '!=', rental.id),
                ('bike_id', '=', rental.bike_id.id),
                ('state', '=', 'confirmed'),
                ('start_date', '<=', rental.expected_return_date),
                ('expected_return_date', '>=', rental.start_date),
            ], limit=1)

            if conflicting_rental:
                raise ValidationError(
                    'This bike is already rented during the selected period.'
                )
            
            in_progress_repair = self.env['bike.workshop.repair'].search([
                ('bike_id', '=', rental.bike_id.id),
                ('bike_source', '=', 'workshop'),
                ('state', '=', 'in_progress'),
            ], limit=1)

            if in_progress_repair:
                raise ValidationError(
                    'This bike cannot be rented because it has an '
                    'In Progress Repair.'
                )

            rental.state = 'confirmed'

    def action_return(self):
        for rental in self:
            if rental.state != 'confirmed':
                raise ValidationError(
                    'Only Confirmed Rentals can be returned.'
                )

            rental.state = 'returned'
            rental.actual_return_date = fields.Date.today()

    @api.depends('start_date', 'expected_return_date')
    def _compute_duration(self):
        for rental in self:
            if rental.start_date and rental.expected_return_date:
                rental.duration = (
                    rental.expected_return_date - rental.start_date
                ).days
            else:
                rental.duration = 0

    @api.depends('duration', 'daily_price')
    def _compute_total_amount(self):
        for rental in self:
            rental.total_amount = rental.duration * rental.daily_price

    @api.onchange('start_date', 'expected_return_date')
    def _onchange_dates(self):
        if (
            self.start_date
            and self.expected_return_date
            and self.expected_return_date <= self.start_date
        ):
            return {
                'warning': {
                    'title': 'Invalid Dates',
                    'message': (
                        'Expected Return Date must be after '
                        'Rental Start Date.'
                    ),
                }
            }

    @api.constrains('start_date', 'expected_return_date')
    def _check_dates(self):
        for rental in self:
            if (
                rental.start_date
                and rental.expected_return_date
                and rental.expected_return_date <= rental.start_date
            ):
                raise ValidationError(
                    'Expected Return Date must be after '
                    'Rental Start Date.'
                )

    @api.constrains('daily_price', 'duration', 'total_amount')
    def _check_positive_values(self):
        for rental in self:
            if rental.daily_price < 0:
                raise ValidationError(
                    'Daily Rental Price cannot be negative.'
                )

            if rental.duration <= 0:
                raise ValidationError(
                    'Rental Duration must be greater than zero.'
                )

            if rental.total_amount < 0:
                raise ValidationError(
                    'Total Rental Amount cannot be negative.'
                )

    @api.onchange('bike_id')
    def _onchange_bike(self):
        if self.bike_id:
            self.daily_price = self.bike_id.daily_rental_price