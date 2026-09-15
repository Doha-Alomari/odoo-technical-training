from odoo.http import route, request
from odoo.addons.portal.controllers.portal import CustomerPortal


class BikeWorkshopPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)


       if 'rental_count' in counters:
            if 'rental_count' in counters:
                partner = request.env.user.partner_id

                values['rental_count'] = request.env[
                    'bike.workshop.rental'
                ].search_count([
                    ('customer_id', '=', partner.id),
                ])

            return values

    @route(
        '/my/rentals',
        type='http',
        auth='user',
        website=True,
    )
    def portal_my_rentals(self, **kwargs):
        partner = request.env.user.partner_id

        rentals = request.env['bike.workshop.rental'].search([
            ('customer_id', '=', partner.id),
        ])

        values = {
            'rentals': rentals,
            'page_name': 'my_rentals',
        }

        return request.render(
            'bike_workshop.portal_my_rentals',
            values,
        )

    @route(
        '/my/rentals/<int:rental_id>',
        type='http',
        auth='user',
        website=True,
    )
    def portal_my_rental(self, rental_id, **kwargs):
        partner = request.env.user.partner_id

        rental = request.env['bike.workshop.rental'].search([
            ('id', '=', rental_id),
            ('customer_id', '=', partner.id),
        ], limit=1)

        if not rental:
            return request.not_found()

        values = {
            'rental': rental,
            'page_name': 'my_rentals',
        }

        return request.render(
            'bike_workshop.portal_my_rental',
            values,
        )