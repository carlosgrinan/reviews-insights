/** @odoo-module */
import { Component, onWillStart, useState } from "@odoo/owl";
import { useService, } from "@web/core/utils/hooks";

export class Card extends Component {
    setup() {
        console.log("3");
        this.orm = useService("orm");
        this.rpc = useService("rpc");
        this.source = this.props.source;

        this.state = useState({
            summary: this.source.summary,
            codeClient: null,
            configId: this.source.config_id,
        });

        onWillStart(async () => {
            if (this.source.scope) {
                this.props.googleScriptLoaded.then(() => {
                    console.log("4");
                    // let intervalId = setInterval(() => {
                    //     if (window.google && window.google.accounts) {
                    //         clearInterval(intervalId);

                    this.state.codeClient = window.google.accounts.oauth2.initCodeClient({
                        client_id: '530981074278-kl9bg74l6at210cj5v18vfckmsqe6c9d.apps.googleusercontent.com', // TODO
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
                    console.log("5");
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
        this.orm.searchRead('reviews_insights.source', [["id", "=", this.source.id]], ['summary']).then(
            (results) => {
                this.state.summary = results[0].summary;
            });
    }

}

Card.template = "reviews_insights.Card";