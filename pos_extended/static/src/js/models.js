odoo.define('pos.pos_extended_models', function (require) {
"use strict";
    const rpc = require('web.rpc');
    var models = require('point_of_sale.models');
    models.load_fields('res.company', ['street', 'street2','state_id', 'country_id', 'city', 'zip']);
    models.load_fields('res.partner',['l10n_in_gst_treatment','title', 'type' ,'is_company']);
    models.load_fields("pos.order", ['with_effort', 'salesman_id']);
    var _super_ordermodel = models.Order.prototype;
    models.Order = models.Order.extend({
        export_for_printing: function(){
            var receipt = _super_ordermodel.export_for_printing.apply(this, arguments);
            this.get_ack_no_and_irn_no(receipt);
            receipt.company.street = this.pos.company.street;
            receipt.company.street2 = this.pos.company.street2;
            receipt.company.country = this.pos.company.country_id;
            receipt.company.state = this.pos.company.state_id;
            receipt.company.city = this.pos.company.city;
            receipt.company.zip = this.pos.company.zip;
            receipt.invoice_no = this.pos.invoice_no
            receipt.invoice_date = this.pos.invoice_date
            receipt.AckNo = this.pos.AckNo
            receipt.Irn = this.pos.Irn
            receipt.qr_code = this.pos.qr_code
            receipt.session_id = this.pos.session_id
            receipt.pos_order_id = this.pos.pos_order_id
            receipt.order_date = this.pos.order_date
            receipt.company_title = this.pos.company_title
            receipt.company_street = this.pos.company_street
            receipt.company_street2 = this.pos.company_street2
            receipt.company_city = this.pos.company_city
            receipt.company_state_id = this.pos.company_state_id
            receipt.company_zip = this.pos.company_zip
            receipt.company_country_id = this.pos.company_country_id
            return receipt;
        },
        get_ack_no_and_irn_no(receipt) {
            var self = this;
            rpc.query({
                model: 'pos.order',
                method: 'get_ack_no_and_irn_no',
                args: [receipt],
            }).then(function (result) {
                if (!result.error) {
                    if (result){
                        self.pos['invoice_no'] = result['invoice_no']
                        self.pos['invoice_date'] = result['invoice_date']
                        self.pos['session_id'] = result['session_id']
                        self.pos['pos_order_id'] = result['pos_order_id']
                        self.pos['order_date'] = result['order_date']
                        self.pos['company_title'] = result['company_title']
                        self.pos['company_street'] = result['company_street']
                        self.pos['company_street2'] = result['company_street2']
                        self.pos['company_city'] = result['company_city']
                        self.pos['company_state_id'] = result['company_state_id']
                        self.pos['company_zip'] = result['company_zip']
                        self.pos['company_country_id'] = result['company_country_id']
                        if (result['AckNo']){
                            self.pos['AckNo'] = result['AckNo']
                        }
                        if (result['Irn']){
                            self.pos['Irn'] = result['Irn']
                        }
                        if (result['QrCode']){
                            const codeWriter = new window.ZXing.BrowserQRCodeSvgWriter()
                            let qr_values = result['QrCode']
                            let qr_code_svg = new XMLSerializer().serializeToString(codeWriter.write(qr_values, 150, 150));
                            self.pos['qr_code'] = "data:image/svg+xml;base64," + window.btoa(qr_code_svg);
                        }
                    }
                } else {
                    self.$el.find("label.error-msg").html(result.error).fadeOut(3000, function () {
                        $(this).html("");
                        $(this).show();//reset the label after fadeout
                    });
                }
            });
        },
        /* ---- With effort button toggle --- */
        set_effort: function(with_effort) {
            this.assert_editable();
            this.with_effort = with_effort;
        },
        is_effort: function(){
            return this.with_effort;
        },

    });

    models.load_models([{
        model:  'hr.employee',
        fields: [],
        domain: function(self){ return [['id','in',self.config.authorized_salesman_ids]]; },
        loaded: function(self, authorizedSalesmans){
            self.authorizedSalesmans = authorizedSalesmans;
        }
    }]);

    var _super_order = models.Order.prototype;
    models.Order = models.Order.extend({
        initialize: function(attr,options) {
            _super_order.initialize.apply(this,arguments);
            this.with_effort = this.with_effort;
            this.salesman_id = this.salesman_id;
            this.save_to_db();
        },
        export_as_JSON: function() {
            var json = _super_order.export_as_JSON.apply(this,arguments);
            json.with_effort = this.with_effort || false;
            json.salesman_id = this.salesman_id ? this.salesman_id.id : false;
            return json;
        },
        init_from_JSON: function(json) {
            _super_order.init_from_JSON.apply(this,arguments);
            this.with_effort =  json.with_effort;
            this.salesman_id = json.salesman_id;
        },
    });

});