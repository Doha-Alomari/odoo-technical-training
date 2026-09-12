from odoo import models, fields
from .service_mixin import ServiceInfoMixin


class Bike(ServiceInfoMixin, models.Model):
    _name = 'bike.workshop.bike'
    _description = 'Bike'

    name = fields.Char(
        string='Bike Name',
        required=True,
    )

    brand = fields.Char(
        string='Brand',
        required=True,
    )

    bike_type = fields.Selection(
        [
            ('road', 'Road'),
            ('mountain', 'Mountain'),
            ('city', 'City'),
            ('electric', 'Electric'),
        ],
        string='Bike Type',
        required=True,
    )

    purchase_date = fields.Date(
        string='Purchase Date',
        required=True,
    )

    last_maintenance_date = fields.Date(
        string='Last Maintenance Date',
        required=True,
    )

    daily_rental_price = fields.Float(
        string='Daily Rental Price',
        required=True,
    )

    wheel_size = fields.Float(
        string='Wheel Size (inches)',
        required=True,
    )

    rental_count = fields.Integer(
        string='Rental Count',
        compute='_compute_rental_count',
    )

    def _compute_rental_count(self):
        for bike in self:
            bike.rental_count = self.env['bike.workshop.rental'].search_count([
                ('bike_id', '=', bike.id),
            ])

    def action_view_rentals(self):
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Rentals',
            'res_model': 'bike.workshop.rental',
            'view_mode': 'list,form',
            'domain': [('bike_id', '=', self.id)],
            'context': {
                'default_bike_id': self.id,
            },
        }