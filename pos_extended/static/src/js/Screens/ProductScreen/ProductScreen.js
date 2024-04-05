odoo.define('pos_extended.ProductScreen', function (require) {
    'use strict';

    const ProductScreen = require('point_of_sale.ProductScreen')
    const Registries = require('point_of_sale.Registries');
    const rpc = require('web.rpc');
    debugger;
    const PosEptProductScreen = (ProductScreen) =>
        class extends ProductScreen {
            set_partner_warning(currentClient,currentScreen) {
                var self = this;
                rpc.query({
                    model: 'pos.order',
                    method: 'set_partner_warning',
                    args: [currentClient,currentScreen],
                }).then(function (result) {
                    if (result){
                        if(Object.keys(result['warning']['partner_data']).length == 0){
                           self.currentOrder.set_client(null);
                        }
                        self.showPopup('ErrorPopup', {
                         title:result['warning']['title'],
                         body: _.str.sprintf(result['warning']['message']),
                        });
                    }
                })
            };

            async _onClickCustomer() {
                // IMPROVEMENT: This code snippet is very similar to selectClient of PaymentScreen.
                const currentClient = this.currentOrder.get_client();
                if (currentClient && this.currentOrder.getHasRefundLines()) {
                    this.showPopup('ErrorPopup', {
                        title: this.env._t("Can't change customer"),
                        body: _.str.sprintf(
                            this.env._t(
                                "This order already has refund lines for %s. We can't change the customer associated to it. Create a new order for the new customer."
                            ),
                            currentClient.name
                        ),
                    });
                    return;
                }
                const { confirmed, payload: newClient } = await this.showTempScreen(
                    'ClientListScreen',
                    { client: currentClient }
                );
                if (confirmed) {
                    this.currentOrder.set_client(newClient);
                    this.currentOrder.updatePricelist(newClient);
                }
                if (newClient){
                  this.set_partner_warning(newClient,this.__owl__.vnode.data.class);
                }
            }
        };
    Registries.Component.extend(ProductScreen, PosEptProductScreen);
    return ProductScreen;
});