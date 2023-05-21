/** @odoo-module **/

import { loadJS } from "@web/core/assets";
import { registry } from "@web/core/registry";
import { onWillStart, useService } from "@web/core/utils/hooks";
import { Card } from "../card/card";

const { Component } = owl;

class Dashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.state = useState({ loadError: false, });


        onWillStart(async () => {
            this.sources = await this.orm.searchRead('proyecto_dam.source', [], ['id', 'display_name', 'summary', 'name', 'scope']);
            this.googleScriptLoaded = loadJS("https://accounts.google.com/gsi/client").catch((error) => {
                console.error(error);
                this.state.loadError = true;
            });

        });
    }

}

Dashboard.components = { Card };
Dashboard.template = "proyecto_dam.clientaction";

registry.category("actions").add("proyecto_dam.dashboard", Dashboard);