/** @odoo-module */
import { Component, onWillStart, useState } from "@odoo/owl";
import { useService, } from "@web/core/utils/hooks";

export class Card extends Component {
    setup() {
        this.source = this.props.source;

        this.state = useState({
            summary: this.source.summary,
            codeClient: null,
            configId: this.source.config_id,
        });

        this.orm = useService("orm");
        this.rpc = useService("rpc");

        // this.bus_service = useService("bus_service");
        // this.channel = this.source.name;
        // this.bus_service.addChannel(this.channel);
        // this.bus_service.addEventListener(
        //     "notification",
        //     this.onNotification.bind(this)
        // );



        onWillStart(async () => {
            if (this.source.scope) {
                this.props.googleScriptLoaded.then(() => {
                    // let intervalId = setInterval(() => {
                    //     if (window.google && window.google.accounts) {
                    //         clearInterval(intervalId);

                    this.state.codeClient = window.google.accounts.oauth2.initCodeClient({
                        client_id: '530981074278-kl9bg74l6at210cj5v18vfckmsqe6c9d.apps.googleusercontent.com',
                        scope: this.source.scope,
                        ux_mode: 'popup',
                        callback: (response) => {
                            if (response.error) {
                                console.error(response.error);
                                console.error(response.description);
                                console.error(response.error_uri);
                            } else {
                                this.rpc('/reviews_insights/oauth2', {
                                    id: this.source.id,
                                    code: response.code,
                                    config_id: this.state.configId,
                                }).then(async () => this.refresh());
                            }
                        }

                    });
                    // }
                    // }, 100);
                });
            }

        });
    }

    disconnect() {
        this.state.summary = null;
        this.state.configId = null;
        this.orm.write('reviews_insights.source', [this.source.id],
            { summary: null, last_refresh: null, refresh_token: null, config_id: null });

    }

    connect() {
        if (this.source.scope) {
            this.state.codeClient.requestCode();
        }
        else {
            this.orm.write('reviews_insights.source', [this.source.id], { config_id: this.state.configId }).then(async () => this.refresh());
        }
    }

    refresh() {
        this.orm.silent.searchRead('reviews_insights.source', [["id", "=", this.source.id]], ['summary']).then(
            (results) => {
                this.state.summary = results[0].summary;

                // Check the result and repeat if necessary
                if (this.state.summary === "Generating summary...") {
                    // Wait for a certain delay (e.g., 2 seconds)
                    setTimeout(() => {
                        // Call the function again
                        this.refresh();
                    }, 3000); // Delay in milliseconds
                }
            });
    }


    // onNotification({ detail: notifications }) {
    //     for (const { payload, type } of notifications) {
    //         if (type === this.source.name) {
    //             console.log(payload);
    //             console.log(payload.message_key);
    //             this.state.summary = payload.message_key;
    //         }
    //     }
    // }
}

Card.template = "reviews_insights.Card";