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
            connected: this.source.connected,
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

        this.needsOAuth = !!this.source.scope



        onWillStart(async () => {

            if (this.state.connected) {
                this.refresh();
            }

            if (this.needsOAuth) {
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
                                this.state.connected = true;

                                this.rpc('/reviews_insights/oauth2', {
                                    id: this.source.id,
                                    code: response.code,
                                    config_id: this.state.configId,
                                    connected: this.state.connected,
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
        this.state.connected = false;
        this.state.summary = null;
        this.state.configId = null;
        this.orm.write('reviews_insights.source', [this.source.id],
            { summary: this.state.summary, last_refresh: null, refresh_token: null, config_id: this.state.configId, connected: this.state.connected });

    }

    connect() {
        if (this.needsOAuth) {
            this.state.codeClient.requestCode();
        }
        else {
            this.state.connected = true;

            this.orm.write('reviews_insights.source', [this.source.id], {
                config_id: this.state.configId, connected: this.state.connected
            }).then(async () => this.refresh());


        }
    }

    refresh() {
        this.orm.silent.searchRead('reviews_insights.source', [["id", "=", this.source.id]], ['summary', 'generating_summary']).then(
            (results) => {
                generatingSummary = results[0].generating_summary;

                if (generatingSummary) {
                    // placeholder
                    if (!this.state.summary) {
                        this.state.summary = _t("Generating summary...");
                    }

                    setTimeout(() => {
                        this.refresh();
                    }, 3000);
                }
                else {
                    this.state.summary = results[0].summary;
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