///** @odoo-module **/
//
//import { _t } from "@web/core/l10n/translation";
//import { PartnerListScreen } from "@point_of_sale/app/screens/partner_list/partner_list";
//import { patch } from "@web/core/utils/patch";
//import { SelectionPopup } from "@point_of_sale/app/utils/input_popups/selection_popup";
//import { useService } from "@web/core/utils/hooks";
//
//
//patch(PartnerListScreen.prototype, {
//    setup() {
//        super.setup(...arguments);
//        this.popup = useService("popup");
//    },
//    confirm() {
//        super.setup(...arguments);
//        if (this.currentOrder.selectPartner() == null && this.currentOrder.is_to_invoice() == false){
//            this.currentOrder.set_to_invoice(!this.currentOrder.is_to_invoice());
//            this.render();
//        }
//        this.props.resolve({ confirmed: true, payload: this.state.selectedPartner });
//        this.pos.closeTempScreen();
//    }
//});
