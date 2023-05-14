/** @odoo-module */
import { useService } from "@web/core/utils/hooks";
const { Component, onWillStart } = owl;

export class Card extends Component {

    setup() {
        // onWillStart(() => {
        //     return loadJS(["https://accounts.google.com/gsi/client"]);

        // });

        // onMounted(() => {
        //     this.client = google.accounts.oauth2.initCodeClient({
        //         client_id: '530981074278-kl9bg74l6at210cj5v18vfckmsqe6c9d.apps.googleusercontent.com',
        //         scope: '{{ context.scopes[0] }}',
        //         ux_mode: 'popup',
        //         callback: (response) => {
        //             const xhr = new XMLHttpRequest();
        //             xhr.open('POST', '/oauth', true);
        //             xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        //             xhr.setRequestHeader('X-Requested-With', 'XmlHttpRequest');
        //             xhr.onload = function () {
        //                 // console.log('Auth code response: ' + xhr.responseText);
        //                 // document.getElementById('emails_summary').innerHTML = xhr.responseText;
        //             };
        //             xhr.send('code=' + response.code);
        //         },
        //     });
        // });
        this.orm = useService("orm");
        this.source = this.props.source;
    }

    async updateSource() {
        const newData = { name: 'New Name' };
        await this.orm.write('proyecto_dam.source', [this.source.id], newData);
        console.log('Source updated successfully');
    }
}

Card.template = "proyecto_dam.Card";