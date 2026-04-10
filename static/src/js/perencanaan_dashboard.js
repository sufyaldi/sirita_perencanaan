/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";

export class PerencanaanDashboard extends Component {
    static template = "sirita_perencanaan.PerencanaanDashboard";

    setup() {
        this.orm = useService("orm");
        this.state = useState({
            stats: {
                states: { draft: 0, review: 0, done: 0 },
                iku_data: [],
                top_depts: []
            }
        });

        onWillStart(async () => {
            await this.loadStats();
        });
    }

    async loadStats() {
        const data = await this.orm.call(
            "sirita.perencanaan.anggaran",
            "get_perencanaan_stats",
            []
        );
        this.state.stats = data;
    }

    formatCurrency(amount) {
        return new Intl.NumberFormat('id-ID', {
            style: 'currency',
            currency: 'IDR',
            minimumFractionDigits: 0
        }).format(amount);
    }
}

registry.category("actions").add("perencanaan_dashboard_action", PerencanaanDashboard);
