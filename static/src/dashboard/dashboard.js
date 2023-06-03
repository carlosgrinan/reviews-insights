/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { loadJS } from "@web/core/assets";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Card } from "../card/card";

class Dashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.state = useState({ loadError: false, });


        onWillStart(async () => {
            this.sources = await this.orm.silent.searchRead('reviews_insights.source', [], ['id', 'display_name', 'summary', 'name', 'scope', 'config_id'],);
            this.googleScriptLoaded = loadJS("https://accounts.google.com/gsi/client").catch((error) => {
                console.error(error);

                this.state.loadError = true;
            });

        });
    }

}

Dashboard.components = { Card };
Dashboard.template = "reviews_insights.clientaction";

registry.category("actions").add("reviews_insights.dashboard", Dashboard);