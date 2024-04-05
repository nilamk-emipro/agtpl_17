odoo.define('pos_extended.ReceiptScreen', function (require) {
    'use strict';

    const ReceiptScreen = require('point_of_sale.ReceiptScreen')
    const Registries = require('point_of_sale.Registries');

    const PosEptReceiptScreen = (ReceiptScreen) =>
        class extends ReceiptScreen {
            mounted() {
                setTimeout(async () => {
                    await this.onSendEmail();
                }, 0);
            }
        };
    Registries.Component.extend(ReceiptScreen, PosEptReceiptScreen);
    return ReceiptScreen;
});
