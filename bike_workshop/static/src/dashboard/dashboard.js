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

    async openActiveRentals() {
        const action = await this.orm.call(
            "bike.workshop.dashboard",
            "action_view_active_rentals",
            []
        );

        this.action.doAction(action);
    }

    async openReturnsDue() {
        const action = await this.orm.call(
            "bike.workshop.dashboard",
            "action_view_returns_due",
            []
        );

        this.action.doAction(action);
    }

    async openRepairsInProgress() {
        const action = await this.orm.call(
            "bike.workshop.dashboard",
            "action_view_repairs_in_progress",
            []
        );

        this.action.doAction(action);
    }
}

registry.category("actions").add(
    "bike_workshop.dashboard",
    WorkshopDashboard
);