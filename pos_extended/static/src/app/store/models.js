/** @odoo-module */

import { Order } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";

patch(Order.prototype, {
    setup(_defaultObj, options) {
        super.setup(...arguments);
        debugger;
        this.salesman_id = null;
        this.with_effort = false;
        debugger;
        if (options.json && options.json.salesman_id) {
            this.salesman_id = options.json.salesman_id || null;
        }
        if (options.json && options.json.with_effort) {
            this.with_effort = options.json.with_effort || false;
        }
    },
    set_salesman(salesman_id) {
        this.salesman_id = salesman_id;
    },
    get_salesman() {
        return this.salesman_id;
    },
    set_effort(with_effort){
        this.with_effort = with_effort;
    },
    is_effort(){
        return this.with_effort;
    },
    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        this.salesman_id = json.salesman_id;
        this.with_effort = json.with_effort;
    },
    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        json["salesman_id"] = this.salesman_id && this.salesman_id.id
        json["with_effort"] = this.with_effort || false
        return json;
    },
//    export_for_printing() {
//    console.log('export_for_printing')
//
//    const receipt = super.export_for_printing(...arguments);
//    this.get_ack_no_and_irn_no(receipt)
//    return receipt;
//    },
//    async get_ack_no_and_irn_no(receipt){
//
//        const loadOrderData = await this.pos.orm.call("pos.order", "get_ack_no_and_irn_no", [
//            [receipt],
//        ]);
//        console.log(loadOrderData)
//        /*if (loadOrderData){
//            debugger
//            self.pos['invoice_no'] = result['invoice_no']
//            self.pos['invoice_date'] = result['invoice_date']
//            self.pos['session_id'] = result['session_id']
//            self.pos['pos_order_id'] = result['pos_order_id']
//            self.pos['order_date'] = result['order_date']
//            self.pos['company_title'] = result['company_title']
//            self.pos['company_street'] = result['company_street']
//            self.pos['company_street2'] = result['company_street2']
//            self.pos['company_city'] = result['company_city']
//            self.pos['company_state_id'] = result['company_state_id']
//            self.pos['company_zip'] = result['company_zip']
//            self.pos['company_country_id'] = result['company_country_id']
//            if (result['AckNo']){
//                self.pos['AckNo'] = result['AckNo']
//            }
//            if (result['Irn']){
//                self.pos['Irn'] = result['Irn']
//            }
//            if (result['QrCode']){
//                const codeWriter = new window.ZXing.BrowserQRCodeSvgWriter()
//                let qr_values = result['QrCode']
//                let qr_code_svg = new XMLSerializer().serializeToString(codeWriter.write(qr_values, 150, 150));
//                self.pos['qr_code'] = "data:image/svg+xml;base64," + window.btoa(qr_code_svg);
//            }
//        }
//        else
//        {
//            const title = _t(loadOrderData.error);
//            const body = _t("");
//            await this.popup.add(ErrorPopup, { title, body });
//        }
//    }*/
//    }
});