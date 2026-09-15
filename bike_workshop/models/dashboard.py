from odoo import api, fields, models


class WorkshopDashboard(models.TransientModel):
    _name = 'bike.workshop.dashboard'
    _description = 'Workshop Operations Dashboard'

    active_rentals_today = fields.Integer(
        string='Active Rentals Today',
        compute='_compute_dashboard_counts',
    )

    returns_due_today = fields.Integer(
        string='Returns Due Today',
        compute='_compute_dashboard_counts',
    )

    repairs_in_progress = fields.Integer(
        string='Repairs In Progress',
        compute='_compute_dashboard_counts',
    )

    @api.depends()
    def _compute_dashboard_counts(self):
        for dashboard in self:
            today = fields.Date.today()

            dashboard.active_rentals_today = self.env[
                'bike.workshop.rental'
            ].search_count([
                ('state', '=', 'confirmed'),
                ('start_date', '<=', today),
                ('expected_return_date', '>=', today),
            ])

            dashboard.returns_due_today = self.env[
                'bike.workshop.rental'
            ].search_count([
                ('state', '=', 'confirmed'),
                ('expected_return_date', '=', today),
            ])

            dashboard.repairs_in_progress = self.env[
                'bike.workshop.repair'
            ].search_count([
                ('state', '=', 'in_progress'),
            ])

    @api.model
    def get_dashboard_data(self):
        today = fields.Date.today()

        return {
            'active_rentals_today': self.env[
                'bike.workshop.rental'
            ].search_count([
                ('state', '=', 'confirmed'),
                ('start_date', '<=', today),
                ('expected_return_date', '>=', today),
            ]),
            'returns_due_today': self.env[
                'bike.workshop.rental'
            ].search_count([
                ('state', '=', 'confirmed'),
                ('expected_return_date', '=', today),
            ]),
            'repairs_in_progress': self.env[
                'bike.workshop.repair'
            ].search_count([
                ('state', '=', 'in_progress'),
            ]),
        }

    def action_view_active_rentals(self):
        today = fields.Date.today()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Active Rentals Today',
            'res_model': 'bike.workshop.rental',
            'view_mode': 'list,form',
            'domain': [
                ('state', '=', 'confirmed'),
                ('start_date', '<=', today),
                ('expected_return_date', '>=', today),
            ],
        }

    def action_view_returns_due(self):
        today = fields.Date.today()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Returns Due Today',
            'res_model': 'bike.workshop.rental',
            'view_mode': 'list,form',
            'domain': [
                ('state', '=', 'confirmed'),
                ('expected_return_date', '=', today),
            ],
        }

    def action_view_repairs_in_progress(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Repairs In Progress',
            'res_model': 'bike.workshop.repair',
            'view_mode': 'list,form',
            'domain': [
                ('state', '=', 'in_progress'),
            ],
        }