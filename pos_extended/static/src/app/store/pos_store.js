/** @odoo-module */

import { Component , markRaw, reactive} from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { SelectionPopup } from "@point_of_sale/app/utils/input_popups/selection_popup";
import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";


patch(PosStore.prototype, {
    //@override
    async _processData(loadedData) {
        await super._processData(...arguments);
        if (this.company.country?.code === 'MX') {
            this.l10n_mx_edi_fiscal_regime = loadedData["l10n_mx_edi_fiscal_regime"];
            this.l10n_mx_country_id = loadedData["l10n_mx_country_id"];
            this.l10n_mx_edi_usage = loadedData["l10n_mx_edi_usage"];
        }
    },
    async selectPartner() {

        const currentOrder = this.get_order();
        if (!currentOrder) {
            return;
        }
        const currentPartner = currentOrder.get_partner();
        if (currentPartner && currentOrder.getHasRefundLines()) {
            this.popup.add(ErrorPopup, {
                title: _t("Can't change customer"),
                body: _t(
                    "This order already has refund lines for %s. We can't change the customer associated to it. Create a new order for the new customer.",
                    currentPartner.name
                ),
            });
            return;
        }
        const { confirmed, payload: newPartner } = await this.showTempScreen("PartnerListScreen", {
            partner: currentPartner,
        });
        if (newPartner){
            debugger;
            const is_product_screen = $('.product-screen').length;
            const loadedWarningDetails = await this.orm.call("pos.order", "set_partner_warning", [newPartner,is_product_screen],
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

            currentOrder.set_partner(newPartner);
        }

    }
});

