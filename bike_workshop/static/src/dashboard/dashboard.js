/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class WorkshopDashboard extends Component {
    static template = "bike_workshop.WorkshopDashboard";

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");

        this.dashboardData = useState({
            active_rentals_today: 0,
            returns_due_today: 0,
            repairs_in_progress: 0,
        });

        onWillStart(async () => {
            const data = await this.orm.call(
                "bike.workshop.dashboard",
                "get_dashboard_data",
                []
            );

            this.dashboardData.active_rentals_today =
                data.active_rentals_today;

            this.dashboardData.returns_due_today =
                data.returns_due_today;

            this.dashboardData.repairs_in_progress =
                data.repairs_in_progress;
        });
    }

    openActiveRentals() {
        const today = luxon.DateTime.now().toISODate();

        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Active Rentals Today",
            res_model: "bike.workshop.rental",
            views: [[false, "list"], [false, "form"]],
            domain: [
                ["state", "=", "confirmed"],
                ["start_date", "<=", today],
                ["expected_return_date", ">=", today],
            ],
        });
    }

    openReturnsDue() {
        const today = luxon.DateTime.now().toISODate();

        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Returns Due Today",
            res_model: "bike.workshop.rental",
            views: [[false, "list"], [false, "form"]],
            domain: [
                ["state", "=", "confirmed"],
                ["expected_return_date", "=", today],
            ],
        });
    }

    openRepairsInProgress() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Repairs In Progress",
            res_model: "bike.workshop.repair",
            views: [[false, "list"], [false, "form"]],
            domain: [
                ["state", "=", "in_progress"],
            ],
        });
    }
}

registry.category("actions").add(
    "bike_workshop.dashboard",
    WorkshopDashboard
);