/** @odoo-module */
import { useService } from "@web/core/utils/hooks";
import { loadJS } from "@web/core/assets";
const { Component, onWillStart } = owl;

export class Card extends Component {

    setup() {
        this.orm = useService("orm");
        this.rpc = useService("rpc");
        this.source = this.props.source;

        onWillStart(async () => {
            loadJS(["https://accounts.google.com/gsi/client"]).then(() => {
                let intervalId = setInterval(() => {
                    if (window.google && window.google.accounts) {
                        clearInterval(intervalId);
                        this.client = window.google.accounts.oauth2.initCodeClient({
                            client_id: '530981074278-kl9bg74l6at210cj5v18vfckmsqe6c9d.apps.googleusercontent.com',
                            scope: 'https://www.googleapis.com/auth/gmail.readonly',
                            ux_mode: 'popup',
                            callback: (response) => {
                                console.log(response);
                                console.log(response.code);
                                this.rpc('/proyecto_dam/oauth2', { code: response.code }).then(() => {

                                    // TODO this.orm.searchRead y me vuelvo a traer el summary, habria que hacer que el summary fuera un useState o algo asi para que se actualice la UI sola
                                });
                                // this.orm.write('proyecto_dam.source', [this.source.id], { code: response.code });

                            },
                        });
                    }
                }, 100);
            });
        });


    }

    requestCode() {
        this.client.requestCode();
    }
}

Card.template = "proyecto_dam.Card";