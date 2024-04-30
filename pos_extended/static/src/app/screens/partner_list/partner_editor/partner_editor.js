/** @odoo-module */

import { usePos } from "@point_of_sale/app/store/pos_hook";
import { PartnerDetailsEdit } from "@point_of_sale/app/screens/partner_list/partner_editor/partner_editor";
import { patch } from "@web/core/utils/patch";
import { Component, useState } from "@odoo/owl";

patch(PartnerDetailsEdit.prototype, {
//    setup() {
//
//        super.setup(...arguments);
//        this.pos = usePos();
//        this.intFields = ['l10n_in_gst_treatment','title', 'company_type' ,'is_company'];
//        const partner = this.props.partner;
//        debugger;
//        this.changes = useState({
//            company_type: partner.company_type || "",
//            l10n_in_gst_treatment: partner.l10n_in_gst_treatment || "",
//            title: partner.title || ""
//        });
//        Object.assign(this.props.imperativeHandle, {
//            save: () => this.saveChanges(),
//        });
//    }
     setup() {
        super.setup(...arguments);
        debugger;
        this.intFields.push('title');
        this.changes.l10n_in_gst_treatment = this.props.partner.l10n_in_gst_treatment || "";
        this.changes.company_type = this.props.partner.company_type || "";
        this.changes.title = this.props.partner.title && this.props.partner.title[0] || "";
//        debugger;
//        Object.assign(this.props.imperativeHandle, {
//            save: () => this.saveChanges(),
//        });
    },
});
