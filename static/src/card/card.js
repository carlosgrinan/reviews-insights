/** @odoo-module */
import { onWillStart, useService, useState } from "@web/core/utils/hooks";
const { Component } = owl;

export class Card extends Component {
    setup() {
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

                    // let intervalId = setInterval(() => {
                    //     if (window.google && window.google.accounts) {
                    //         clearInterval(intervalId);

                    this.state.codeClient = window.google.accounts.oauth2.initCodeClient({
                        client_id: '530981074278-kl9bg74l6at210cj5v18vfckmsqe6c9d.apps.googleusercontent.com', //TODO preguntar a chatgpt que se hace con eso
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
                                    this.orm.searchRead('proyecto_dam.source', [this.source.id], ['summary']).then((results) => {
                                        this.state.summary = results[0].summary;
                                    });
                                });
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
        this.orm.write('proyecto_dam.source', [this.source.id], { summary: null, refresh_token: null });

    }

    connect() {
        this.state.codeClient.requestCode();
    }

}

Card.template = "proyecto_dam.Card";