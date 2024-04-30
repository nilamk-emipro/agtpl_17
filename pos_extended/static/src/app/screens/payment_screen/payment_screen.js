/** @odoo-module */

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";

patch(PaymentScreen.prototype, {
//    onMounted() {
//        setTimeout(async () => {
//            if (this.currentOrder.selectPartner() != null && this.currentOrder.is_to_invoice() == false){
//                await this.toggleIsToInvoice();
//            }
//            if (this.currentOrder.is_to_invoice() == true && this.currentOrder.toggleIsToInvoice() == null){
//                await this.toggleIsToInvoice();
//            }
//            const currentClient = this.currentOrder.toggleIsToInvoice();
//            if(currentClient){
//                this.set_partner_warning(currentClient);
//            }
//        }, 0);
//    }
    async selectPartner(isEditMode = false, missingFields = []) {
        // IMPROVEMENT: This code snippet is repeated multiple times.
        // Maybe it's better to create a function for it.
        const currentPartner = this.currentOrder.get_partner();
        const partnerScreenProps = { partner: currentPartner };
        if (isEditMode && currentPartner) {
            partnerScreenProps.editModeProps = true;
            partnerScreenProps.missingFields = missingFields;
        }
        const { confirmed, payload: newPartner } = await this.pos.showTempScreen(
            "PartnerListScreen",
            partnerScreenProps
        );
        if (newPartner){
            const is_product_screen = $('.product-screen').length;
            const loadedWarningDetails = await this.orm.call("pos.order", "set_partner_warning",
            [newPartner,is_product_screen]
            );
            if (loadedWarningDetails){
                const title = _t(loadedWarningDetails['warning']['title']);
                const body = _t(loadedWarningDetails['warning']['message']);
                await this.popup.add(ErrorPopup, { title, body });
                if(Object.keys(loadedWarningDetails['warning']['partner_data']).length == 0){
                   return;
            }}
        }
        if (confirmed) {
            this.currentOrder.set_partner(newPartner);
        }
    }
});
