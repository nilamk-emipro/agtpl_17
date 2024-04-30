/** @odoo-module */

import { ReceiptScreen } from "@point_of_sale/app/screens/receipt_screen/receipt_screen";
import { patch } from "@web/core/utils/patch";

patch(ReceiptScreen.prototype, {
    onMounted() {
        setTimeout(async () => {
           await this.onSendEmail();
        }, 0);
    }
});
