odoo.define('pos_extended.ClientListScreen', function (require) {
    'use strict';

    const ClientListScreen = require('point_of_sale.ClientListScreen')
    const Registries = require('point_of_sale.Registries');

    const PosEptClientListScreen = (ClientListScreen) =>
        class extends ClientListScreen {
            confirm() {
                if (this.currentOrder.get_client() == null && this.currentOrder.is_to_invoice() == false){
                    this.currentOrder.set_to_invoice(!this.currentOrder.is_to_invoice());
                    this.render();
                }
                this.props.resolve({ confirmed: true, payload: this.state.selectedClient });
                this.trigger('close-temp-screen');
            }
        };
    Registries.Component.extend(ClientListScreen, PosEptClientListScreen);
    return ClientListScreen;
});

