/** @odoo-module */
import { useService, } from "@web/core/utils/hooks";
import { Component, useState, onWillStart } from "@odoo/owl";

export class Card extends Component {
    setup() {
        console.log("3");
        this.orm = useService("orm");
        this.rpc = useService("rpc");
        this.source = this.props.source;

        this.state = useState({
            summary: this.source.summary,
            codeClient: null,
        });

        onWillStart(async () => {
            if (this.source.scope) {
                this.props.googleScriptLoaded.then(() => {
                    console.log("4");
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
                                this.rpc('/proyecto_dam/oauth2', {
                                    id: this.source.id,
                                    code: response.code,
                                }).then(async () => {
                                    this.orm.searchRead('proyecto_dam.source', [["id", "=", this.source.id]], ['summary']).then((results) => {
                                        this.state.summary = results[0].summary;
                                    });
                                });
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
        this.orm.write('proyecto_dam.source', [this.source.id], { summary: null, refresh_token: null, last_refresh: null });

    }

    connect() {
        this.state.codeClient.requestCode();
    }

}

Card.template = "proyecto_dam.Card";