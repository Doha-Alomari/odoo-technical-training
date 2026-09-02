from odoo import models, fields


class Bike(models.Model):
    _name = 'bike.workshop.bike'
    _description = 'Bike'

    name = fields.Char(string='Bike Name', required=True)
    brand = fields.Char(string='Brand', required=True)

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