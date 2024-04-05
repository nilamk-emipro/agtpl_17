odoo.define('pos_extended.PaymentScreen', function (require) {
    'use strict';

    const PaymentScreen = require('point_of_sale.PaymentScreen')
    const Registries = require('point_of_sale.Registries');
    const rpc = require('web.rpc');
    const PosEptPaymentScreen = (PaymentScreen) =>
        class extends PaymentScreen {
            mounted() {
                setTimeout(async () => {
                    if (this.currentOrder.get_client() != null && this.currentOrder.is_to_invoice() == false){
                        await this.toggleIsToInvoice();
                    }
                    if (this.currentOrder.is_to_invoice() == true && this.currentOrder.get_client() == null){
                        await this.toggleIsToInvoice();
                    }
                    const currentClient = this.currentOrder.get_client();
                    if(currentClient){
                        this.set_partner_warning(currentClient,this.__owl__.vnode.data.class);
                    }
                }, 0);
            }
            set_partner_warning(currentClient,currentScreen) {
            var self = this;
                rpc.query({
                    model: 'pos.order',
                    method: 'set_partner_warning',
                    args: [currentClient,currentScreen],
                }).then(function (result) {
                    if (result){
                        if(Object.keys(result['warning']['partner_data']).length == 0){
                           self.currentOrder.set_to_invoice(!self.currentOrder.is_to_invoice());
                           self.render();
                        }
                        self.showPopup('ErrorPopup', {
                         title:result['warning']['title'],
                         body: _.str.sprintf(result['warning']['message']),
                        });
                    }
                })
            };
        };
    Registries.Component.extend(PaymentScreen, PosEptPaymentScreen);
    return PaymentScreen;
});

