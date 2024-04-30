///** @odoo-module */
//
//import { usePos } from "@point_of_sale/app/store/pos_hook";
//import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
//import { Component , markRaw, reactive} from "@odoo/owl";
//import { _t } from "@web/core/l10n/translation";
//import { registry } from "@web/core/registry";
//import { useService } from "@web/core/utils/hooks";
//import { SelectionPopup } from "@point_of_sale/app/utils/input_popups/selection_popup";
//import { Reactive } from "@web/core/utils/reactive";
//import { patch } from "@web/core/utils/patch";
//import { PosStore } from "@point_of_sale/app/store/pos_store";
//import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";


//export class setSalesmanButton extends Reactive {
//    static template = "pos_extended.SetSalesmanButton";
//
//    constructor() {
//        super(...arguments);
////        useListener('click', this.onClick);
//    }
//
//    setup() {
//
//        this.pos = usePos();
//        this.popup = useService("popup");
//        this.orm = useService("orm");
//        this.authorized_salesman_ids = new Set();
////        this.salesman = null;
//    }
//
//    mounted() {
//
//        this.pos.get('orders').on('add remove change', () => this.render(), this);
//        this.pos.on('change:selectedOrder', () => this.render(), this);
//    }
//    willUnmount() {
//
//        this.pos.get('orders').off('add remove change', null, this);
//        this.pos.off('change:selectedOrder', null, this);
//    }
//    get currentOrder() {
//
//        const order = this.pos.get_order();
//        return this.pos.get_order();
//    }
//
//    get currentSelectedSalesmanName() {
//
//        return this.pos.config.auth_salesman_selection && this.currentOrder && this.currentOrder.salesman_id
//            ? this.currentOrder.salesman_id.display_name : null;
//    }
//}



/** @odoo-module */

import { usePos } from "@point_of_sale/app/store/pos_hook";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { Component } from "@odoo/owl";

export class SetSalesmanButton extends Component {
//    static template = "pos_extended.SetSalesmanButton";

    setup() {
        this.pos = usePos();
    }

    get partner() {
        const order = this.pos.get_order();
        return order ? order.get_partner() : null;
    }

    get currentOrder() {
        const order = this.pos.get_order();
        return this.pos.get_order();
    }

    get currentSelectedSalesmanName() {

        return this.pos.config.auth_salesman_selection && this.currentOrder && this.currentOrder.salesman_id
            ? this.currentOrder.salesman_id.display_name : null;
    }
}
//
//ProductScreen.addControlButton({
//    component: SetSalesmanButton,
//    position: ["before", "CustomerButton"],
//    condition: function () {
//        return this.pos.config.authorized_salesman_ids;
//    },
//});
