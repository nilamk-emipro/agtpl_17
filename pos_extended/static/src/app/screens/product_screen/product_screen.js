/** @odoo-module */

import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { _t } from "@web/core/l10n/translation";
import { SelectionPopup } from "@point_of_sale/app/utils/input_popups/selection_popup";
import { patch } from "@web/core/utils/patch";


patch(ProductScreen.prototype, {
    async onClick() {
        const currentSalesman = this.currentOrder.salesman_id;
        const salesmanList = [];
//        const salesmanList = [
//            {
//                id: -1,
//                label: _t("None"),
//                isSelected: !currentSalesman,
//            },
//        ];
//
        const loadedData = await this.orm.call("pos.config", "load_authorized_salesman_ids", [
            [],
        ]);

        for (const salesman_id of loadedData) {

            salesmanList.push({
                id: salesman_id.id,
                label: salesman_id.name,
                isSelected: currentSalesman
                    ? salesman_id.id === currentSalesman.id
                    : false,
                item: salesman_id,
            });
        }
        const { confirmed, payload: selectSalesman } = await this.popup.add(
            SelectionPopup,
            {
                title: _t("Select Salesman"),
                list: salesmanList,
            }
        );
        if (confirmed) {

            /*ToDo*/
            this.currentOrder.set_salesman(selectSalesman);
            this.props.salesman_id = selectSalesman;
            this.salesman_id = selectSalesman;

        }
    },
    async toggleWithEffort() {
        this.currentOrder.set_effort(!this.currentOrder.is_effort());
        this.props.with_effort = this.currentOrder.with_effort;
        this.render();
    },
});
