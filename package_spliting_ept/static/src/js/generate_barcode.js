//odoo.define('package_spliting_ept.MainMenu', function (require) {
//    "use strict";
//    const mobile = require('web_mobile.core');
//    var ajax = require('web.ajax');
//    var core = require('web.core');
//    var concurrency = require('web.concurrency');
//    var AbstractAction = require('web.AbstractAction');
//    var SystrayMenu = require('web.SystrayMenu');
//    var QWeb = core.qweb;
//    var rpc = require('web.rpc');
//    var session = require('web.session');
//    var SplitPackageMainScreen = AbstractAction.extend({
//        custom_events: {
//            exit: '_onClickExit'
//        },
//        events: {
//            'click .o_barcode_message': 'open_mobile_scanner',
//            'click .o_generate_barcode': 'scanBarcode',
//            'click .o_generate_pdf': '_generatePDF',
//            'click .o_generate_picking': '_onClickGeneratePicking',
//        },
//        init: function () {
//            this._super.apply(this, arguments);
//            this.mutex = new concurrency.Mutex();
//            this.db = '';
//        },
//        start: function () {
//            var self = this;
//            this.$('.o_content').addClass('o_barcode_client_action');
//            core.bus.on('barcode_scanned', this, this._onBarcodeScanned);
//            return this._super.apply(this, arguments).then(function () {
//                return Promise.all([
//                  $('<div class="o_content_ept"></div>').appendTo(self.$('.o_content')),
//                ]).then(function () {
//                    self._renderView()
//                });
//            });
//        },
//        _renderView: function () {
//            var $content = $(QWeb.render('package_spliting_ept.MainScreen'));
//            this.$('.o_content_ept').append($content);
//        },
//        _onClickExit: function (ev) {
//            var self = this;
//            this.mutex.exec(function () {
//                window.history.go(-2);
//            });
//        },
//        open_mobile_scanner: function () {
//            var self = this;
//            if (mobile.methods.scanBarcode) {
//                mobile.methods.scanBarcode().then(function (response) {
//                    var barcode = response.data;
//                    if (barcode) {
//                        self.scanBarcode(barcode)
//                    } else {
//                        mobile.methods.showToast({'message': 'Please, Scan again !!'});
//                    }
//                });
//            }
//        },
//        _onBarcodeScanned: function (barcode) {
//            this.scanBarcode(barcode)
//
//        },
//        scanBarcode: function (barcode) {
//            var self = this;
//            self._resetView()
//            if (barcode instanceof Object) {
//                barcode = self.$el.find("input[name='barcode']").val();
//            } else if (typeof (barcode) === "string") {
//                self.$el.find("input[name='barcode']").val(barcode);
//            }
//            if (barcode) {
//                self._onScannedBarcode(barcode)
//            } else {
//                self.$el.find("label.error-msg").html('Please, Scan again !!').fadeOut(3000, function () {
//                    $(this).html("");
//                    $(this).show();//reset the label after fadeout
//                });
//            }
//        },
//        _onScannedBarcode: function (barcode) {
//            var self = this;
//            this._rpc({
//                model: 'package.spliting.barcode',
//                method: 'read_barcode',
//                args: [barcode],
//                limit: 1,
//            }).then(function (result) {
//                if (!result.error) {
//                    self.db = result.database
//                    var html = "<h3>Package Information</h3><hr/>" +
//                        "<form id='package_details' method='post' action='cut_and_generate'>" +
//                        "<div class='row' style='margin-top:10px'>" +
//                        "<div class='col-lg-6'><strong>Name</strong></div>" +
//                        "<div class='col-lg-6'><span>" + result.name[1] + "</span></div>" +
//                        "<input type='hidden' name='package' value='" + result.name[0] + "'/>" +
//                        "</div>" +
//                        "<div class='row' style='margin-top:10px'>" +
//                        "<div class='col-lg-6'><strong>Product</strong></div>" +
//                        "<div class='col-lg-6'><span>" + result.product[1] + "</span></div>" +
//                        "</div>" +
//                        "<input type='hidden' name='product' value='" + result.product + "'/>" +
//                        "<div class='row' style='margin-top:10px'>" +
//                        "<div class='col-lg-6'><strong>Lot number</strong></div>" +
//                        "<div class='col-lg-6'><span>" + result.lot[1] + "</span></div>" +
//                        "</div>" +
//                        "<input type='hidden' name='lot' value='" + result.lot[0] + "'/>" +
//                        "<div class='row' style='margin-top:10px'>" +
//                        "<div class='col-lg-6'><strong>Available Quantity</strong></div>" +
//                        "<div class='col-lg-6'>" +
//                        "<span class='available_quantity'>"+result.quantity+"</span> / <span>" + result.uom[1] +"</span>"+
//                        "</div>" +
//                        "</div>" +
//                        "<div class='row' style='margin-top:10px'>" +
//                        "<div class='col-lg-6'><strong>Quantity To Cut</strong></div>" +
//                        "<div class='col-lg-6'>" +
//                        "<input type='number' style='width:100px;display:inline' name='quantity_to_cut' value='0.0'/> / " + result.uom[1] +
//                        "</div>" +
//                        "</div>" +
//                        "<div class='row mt-2'>" +
//                        "<div class='col-lg-6'>" +
//                        "</div>" +
//                        "<div class='col-lg-6'>" +
//                        "<button type='button' class='btn btn-primary text-uppercase o_generate_picking' name='generate_picking' >" +
//                        "<i class='fa fa-cut mr-1'/> Split Package " +
//                        "</button>" +
//                        "</div>" +
//                        "</div>" +
//                        "</form> ";
//                    self.$('#product_info').html(html);
//                } else {
//                    self.$el.find("label.error-msg").html(result.error).fadeOut(3000, function () {
//                        $(this).html("");
//                        $(this).show();//reset the label after fadeout
//                    });
//                }
//            });
//        },
//        _generatePDF: function (){
//            var barcode_id = parseInt(this.$el.find("input[name='barcode_id']").val())
//            this.do_action({
//                  type: 'ir.actions.report',
//                  report_type: 'qweb-pdf',
//                  report_name: 'stock.report_package_barcode_small/' + barcode_id,
//              });
//        },
//        _resetView: function () {
//            var self = this;
//            self.$('#product_info').html('');
//            self.$('#barcode_info').html('');
//        },
//        _onClickGeneratePicking: function(ev) {
//            var self = this;
//            var form_data = {};
//            $.each($('form#package_details').serializeArray(), function () {
//                form_data[this.name] = this.value;
//            });
//           this._rpc({
//                model: 'package.spliting.barcode',
//                method: 'create_picking',
//                args: [form_data],
//            }).then(function (result) {
//                if (!result.error) {
//                    var html = "<h3 style='display: inline-block;'>Barcode</h3>" +
//                        "<a href='javascript:void(0)' class='pull-right btn btn-link o_generate_pdf' target='_self'>" + //style='cursor: pointer'
//                        "<i class='fa fa-download mr-1' role='img'/>" +
//                        "</a><hr/>" +
//                        "<form id='barcode_details'>" +
//                        "<div class='row'>" +
//                        "<div class='col-lg-12' style='position:relative; display:inline-block'>" +
//                        "<img src='/report/barcode?type=Code128&humanreadable=1&value=" + result.barcode + "' style='display: block; width:100%; margin-left:-36px' class='image-responsive'/>" +
//                        "<input type='hidden' name='barcode' value='" + result.barcode + "'/> " +
//                        "<input type='hidden' name='barcode_id' value='" + result.barcode_id + "'/> " +
//                        "</div>" +
//                        "</div>" +
//                        "</form> ";
//                    self.$('#barcode_info').html(html);
//                    self.$("span.available_quantity").html(result.remaining_qty)
//                    self.$("input[name='quantity_to_cut']").val(0.0)
//                } else {
//                    self.$el.find("label.error-msg").html(result.error).fadeOut(3000, function () {
//                        $(this).html("");
//                        $(this).show();//reset the label after fadeout
//                    });
//                }
//            });
//            console.log('_onClickGeneratePicking : Form Data', form_data);
//        }
//    });
//    core.action_registry.add('package_spliting_main_screen', SplitPackageMainScreen);
//    return SplitPackageMainScreen;
//});
