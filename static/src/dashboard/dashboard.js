/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Card } from "../card/card";


const { Component, onWillStart } = owl;

class Dashboard extends Component {
    setup() {
        this.orm = useService("orm");

        onWillStart(async () => {
            this.sources = await this.orm.searchRead('proyecto_dam.source', [], ['id', 'name', 'summary', 'img_name']);
            console.log(this.sources);
        });
    }

}

Dashboard.components = { Card };
Dashboard.template = "proyecto_dam.clientaction";

registry.category("actions").add("proyecto_dam.dashboard", Dashboard);