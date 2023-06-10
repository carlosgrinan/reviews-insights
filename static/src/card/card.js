/** @odoo-module */
import { Component, onWillStart, useState } from "@odoo/owl";
import { useService, } from "@web/core/utils/hooks";
const { status } = owl;

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
        this.loadError = this.props.loadError



        onWillStart(async () => {

            if (this.state.connected) {
                this.fetch_summary();
            }

            if (this.needsOAuth) {
                this.props.googleScriptLoaded.then(() => {
                    if (!this.loadError) {
                        let intervalId = setInterval(() => {
                            if (window.google && window.google.accounts) {
                                clearInterval(intervalId);

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
                                            this._connect(response.code);
                                        }
                                    }

                                });

                            }
                        }, 100);
                    }
                });
            }

        });
    }

    disconnect() {
        this.state.connected = false;
        this.state.summary = null;
        this.state.configId = null;
        this.orm.write('reviews_insights.source', [this.source.id],
            { summary: this.state.summary, last_refresh: null, refresh_token: null, config_id: this.state.configId, connected: this.state.connected, generating_summary: false });

    }

    connect() {
        if (this.needsOAuth) {
            this.state.codeClient.requestCode();
        }
        else {
            this._connect();
        }
    }

    _connect(code = null) {
        this.state.connected = true;

        this.rpc('/reviews_insights/connect', {
            id: this.source.id,
            code: code,
            config_id: this.state.configId,
            connected: this.state.connected,
        }, {
            silent: true,
        }).then(async () => this.fetch_summary());
    }



    fetch_summary() {
        try {

            //In case the user left the app to use another Odoo app
            if (status(this) != 'destroyed') {

                this.orm.silent.searchRead('reviews_insights.source', [["id", "=", this.source.id]], ['summary', 'generating_summary']).then(
                    (results) => {

                        const generatingSummary = results[0].generating_summary;
                        if (generatingSummary) {

                            setTimeout(() => {

                                this.fetch_summary();

                            }, 3000);
                        }
                        else {
                            this.state.summary = results[0].summary;
                        }
                    });
            }
        } catch (error) {
            console.error(error);
        }

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