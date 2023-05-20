/** @odoo-module */
import { useService, useState } from "@web/core/utils/hooks";
import { loadJS } from "@web/core/assets";
const { Component, onWillStart } = owl;



export class Card extends Component {

    setup() {

        this.orm = useService("orm");
        this.rpc = useService("rpc");
        this.source = this.props.source;
        this.client = null;

        this.state = useState({
            summary: this.source.summary,
        });



        onWillStart(async () => {
            // oauth2
            if (this.source.scope) {
                loadJS(["https://accounts.google.com/gsi/client"]).then(() => {

                    let intervalId = setInterval(() => {
                        if (window.google && window.google.accounts) {
                            clearInterval(intervalId);

                            this.client = window.google.accounts.oauth2.initCodeClient({
                                client_id: '530981074278-kl9bg74l6at210cj5v18vfckmsqe6c9d.apps.googleusercontent.com',
                                scope: this.source.scope,
                                ux_mode: 'popup',
                                callback: (response) => {
                                    if (response.error) {
                                        console.error(response.error);
                                        console.error(response.description);
                                        console.error(response.error_uri);
                                    } else {
                                        this.rpc('/proyecto_dam/oauth2', { code: response.code }).then(() => {
                                            this.state.summary = this.orm.searchRead('proyecto_dam.source', [this.source.id], ['summary']);
                                        });
                                    }
                                }

                            });
                        }
                    }, 100);
                });
            }

        });


    }

    disconnect() {


        //erase ui
        this.state.summary = null;
        //erase db
        this.orm.write('proyecto_dam.source', [this.source.id], { summary: null, refresh_token: null });

    }

    connect() {
        this.client.requestCode();
    }

}

Card.template = "proyecto_dam.Card";