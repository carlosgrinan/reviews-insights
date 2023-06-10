/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { loadJS } from "@web/core/assets";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Card } from "../card/card";

class Dashboard extends Component {
    setup() {
        // get scrolling behavior on odoo main div
        var actionManager = document.querySelector('.o_action_manager');
        actionManager.style.overflow = 'auto';

        this.orm = useService("orm");
        this.state = useState({ internetError: false, });
        this.loadError = false

        // this.bus_service = useService("bus_service");
        // this.channel = "my-channel";
        // this.bus_service.addChannel(this.channel);
        // this.bus_service.addEventListener(
        //     "notification",
        //     this.onNotification.bind(this)
        // );
        // this.bus_service.start();


        onWillStart(async () => {
            this.sources = await this.orm.silent.searchRead('reviews_insights.source', [], [],);
            this.googleScriptLoaded = loadJS("https://accounts.google.com/gsi/client").catch((error) => {
                console.error(error);
                this.state.internetError = true;
                this.loadError = true

            });
        });
    }


    // onNotification({ detail: notifications }) {
    //     for (const { payload, type } of notifications) {
    //         if (type === "my-type") {
    //             console.log(payload);
    //             // console.log(payload.message_key);
    //             // this.state.summary = payload.message_key;
    //         }
    //     }
    // }

}

Dashboard.components = { Card };
Dashboard.template = "reviews_insights.clientaction";

registry.category("actions").add("reviews_insights.dashboard", Dashboard);