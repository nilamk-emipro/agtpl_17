/** @odoo-module **/
import mobile from '@web_mobile/js/services/core';
import { _t } from "@web/core/l10n/translation";
import * as BarcodeScanner from '@web/webclient/barcode/barcode_scanner';
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { registry } from "@web/core/registry";
import { useBus, useService } from "@web/core/utils/hooks";
import { session } from "@web/session";
import { serializeDate, today } from "@web/core/l10n/dates";
import { Component, onWillStart, useState } from "@odoo/owl";
import { scanBarcode, BarcodeDialog } from "@web/webclient/barcode/barcode_scanner";


class MainScreen extends Component {
	setup() {
	    this.rpc = useService('rpc');
        this.orm = useService('orm');
        this.action = useService("action");
	    this.barcodeService = useService('barcode');
        useBus(this.barcodeService.bus, "barcode_scanned", (ev) => this._onBarcodeScanned(ev.detail.barcode));
	}

	async o_generate_barcode(barcode,ev) {
        var self = this;
        self._resetView()
        if (barcode instanceof Object) {
            barcode = $("input[name='barcode']").val();
        } else if (typeof (barcode) === "string") {
            $("input[name='barcode']").val(barcode);
        }
        if (barcode) {
            self._onScannedBarcode(barcode)
        } else {
            self.$el.find("label.error-msg").html('Please, Scan again !!').fadeOut(3000, function () {
                $(this).html("");
                $(this).show();//reset the label after fadeout
            });
        }
    }
    _resetView() {
        var self = this;
        $('#product_info').html('');
        $('#barcode_info').html('');
    }

    async _onScannedBarcode(barcode) {
            var self = this;
            const result = await this.rpc('/package_spliting_ept/get_barcode_data',{ model: 'package.spliting.barcode',barcode: barcode});
            if (!result.error){
                self.db = result.database
                var html = "<h3>Package Information</h3><hr/>" +
                    "<form id='package_details' method='post' action='cut_and_generate'>" +
                    "<div class='row' style='margin-top:10px'>" +
                    "<div class='col-lg-6'><strong>Name</strong></div>" +
                    "<div class='col-lg-6'><span>" + result.name[1] + "</span></div>" +
                    "<input type='hidden' name='package' value='" + result.name[0] + "'/>" +
                    "</div>" +
                    "<div class='row' style='margin-top:10px'>" +
                    "<div class='col-lg-6'><strong>Product</strong></div>" +
                    "<div class='col-lg-6'><span>" + result.product[1] + "</span></div>" +
                    "</div>" +
                    "<input type='hidden' name='product' value='" + result.product + "'/>" +
                    "<div class='row' style='margin-top:10px'>" +
                    "<div class='col-lg-6'><strong>Lot number</strong></div>" +
                    "<div class='col-lg-6'><span>" + result.lot[1] + "</span></div>" +
                    "</div>" +
                    "<input type='hidden' name='lot' value='" + result.lot[0] + "'/>" +
                    "<div class='row' style='margin-top:10px'>" +
                    "<div class='col-lg-6'><strong>Available Quantity</strong></div>" +
                    "<div class='col-lg-6'>" +
                    "<span class='available_quantity'>"+result.quantity+"</span> / <span>" + result.uom[1] +"</span>"+
                    "</div>" +
                    "</div>" +
                    "<div class='row' style='margin-top:10px'>" +
                    "<div class='col-lg-6'><strong>Quantity To Cut</strong></div>" +
                    "<div class='col-lg-6'>" +
                    "<input type='number' style='width:100px;display:inline' name='quantity_to_cut' value='0.0'/> / " + result.uom[1] +
                    "</div>" +
                    "</div>" +
                    "<div class='row mt-2'>" +
                    "<div class='col-lg-6'>" +
                    "</div>" +
//                    "<div class='col-lg-6'>" +
//                    "<button type='button' class='btn btn-primary text-uppercase o_generate_picking' t-on-click='_onClickGeneratePicking'>" +
//                    "<i class='fa fa-cut mr-1'/> Split Package " +
//                    "</button>" +
//                    "</div>" +
                    "</div>" +
                    "</form> ";
                $('#product_info').html(html);
                $('.o_generate_picking').css('display', 'block');
            } else {
                $("label.error-msg").html(result.error).fadeOut(3000, function () {
                    $(this).html("");
                    $(this).show();//reset the label after fadeout
                });
          }
    }

    async _onClickGeneratePicking(ev) {
        var self = this;
        var form_data = {};
        $.each($('form#package_details').serializeArray(), function () {
            form_data[this.name] = this.value;
        });
        const result = await this.rpc('/package_spliting_ept/create_picking',{ model: 'package.spliting.barcode',form_data: form_data});
        if (!result.error) {
                var html = "<h3 style='display: inline-block;'>Barcode</h3>" +
//                    "<a href='javascript:void(0)' class='pull-right btn btn-link o_generate_pdf' target='_self' t-on-click='_generatePDF'>" + //style='cursor: pointer'
//                    "<i class='fa fa-download mr-1' role='img'/>" +
//                    "</a><hr/>" +
                    "<form id='barcode_details'>" +
                    "<div class='row'>" +
                    "<div class='col-lg-12' style='position:relative; display:inline-block'>" +
                    "<img src='/report/barcode?barcode_type=Code128&humanreadable=1&value=" + result.barcode + "' style='display: block; width:100%; margin-left:-36px' class='image-responsive'/>" +
                    "<input type='hidden' name='barcode' value='" + result.barcode + "'/> " +
                    "<input type='hidden' name='barcode_id' value='" + result.barcode_id + "'/> " +
                    "</div>" +
                    "</div>" +
                    "</form> ";
                $('.o_generate_pdf').css('display', 'block');
                $('#barcode_info').html(html);
                $("span.available_quantity").html(result.remaining_qty)
                $("input[name='quantity_to_cut']").val(0.0)
            } else {
                $("label.error-msg").html(result.error).fadeOut(3000, function () {
                    $(this).html("");
                    $(this).show();//reset the label after fadeout
                });
            }

        console.log('_onClickGeneratePicking : Form Data', form_data);
    }

    _generatePDF(){
        var barcode_id = parseInt($("input[name='barcode_id']").val())
        this.action.doAction({
              type: 'ir.actions.report',
              report_type: 'qweb-pdf',
              report_name: 'stock.report_package_barcode_small/' + barcode_id,
          });
    }

    open_mobile_scanner() {
        var self = this;
        if (mobile.methods.scanBarcode) {
            mobile.methods.scanBarcode().then(function (response) {
                var barcode = response.data;
                if (barcode) {
                    self.scanBarcode(barcode)
                } else {
                    mobile.methods.showToast({'message': 'Please, Scan again !!'});
                }
            });
        }
    }

//    _onBarcodeScanned: function (barcode) {
//            this.scanBarcode(barcode)
//
//    }
//
//    scanBarcode(barcode) {
//        var self = this;
//        self._resetView()
//        if (barcode instanceof Object) {
//            barcode = $("input[name='barcode']").val();
//        } else if (typeof (barcode) === "string") {
//            $("input[name='barcode']").val(barcode);
//        }
//        if (barcode) {
//            self._onScannedBarcode(barcode)
//        } else {
//            self.$el.find("label.error-msg").html('Please, Scan again !!').fadeOut(3000, function () {
//                $(this).html("");
//                $(this).show();//reset the label after fadeout
//            });
//        }
//    }
}

MainScreen.props = ["action", "actionId", "className"];
MainScreen.props = {
    action: { Object },
    actionId: { type: Number, optional: true },
    className: String,
    globalState: { type: Object, optional: true },
};

MainScreen.template = 'package_spliting_ept.MainScreen';
registry.category("actions").add("package_splitting_main_screen", MainScreen);
export default MainScreen;