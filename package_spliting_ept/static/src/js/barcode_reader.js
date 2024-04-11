//odoo.define('package_spliting_ept.BarcodeParser',[], function (require) {
//    "use strict";
//
//    var BarcodeReader = require('point_of_sale.BarcodeReader');
//    var models = require('point_of_sale.models');
//    var rpc = require('web.rpc');
//    var core = require('web.core');
//    var _t = core._t;
//
//    BarcodeReader.include({
//        scan: async function (code) {
//            var self = this;
//            if (!code) {
//                return;
//            }
//            const callbacks = Object.keys(this.exclusive_callbacks).length
//            ? this.exclusive_callbacks
//            : this.action_callbacks;
//            let parsed_results = this.barcode_parser.parse_barcode(code);
//            if (! Array.isArray(parsed_results)) {
//                parsed_results = [parsed_results];
//            }
//            for (const parsed_result of parsed_results) {
//                Promise.all([self._getLotInfo(parsed_result)]).then(function (matchedLot) {
//                    console.log(parsed_result)
//                    if (matchedLot[0].length) {
//                        parsed_result['lot'] = matchedLot[0][0]['lot_id'][1];
//                        self.pos.lot_id = matchedLot[0][0]['lot_id'][1];
//                    }
//                })
//                if (callbacks[parsed_result.type]) {
//                    for (const cb of callbacks[parsed_result.type]) {
//                        cb(parsed_result);
//                    }
//                } else if (callbacks.error) {
//                    [...callbacks.error].map(cb => cb(parsed_result));
//                } else {
//                    console.warn('Ignored Barcode Scan:', parsed_result);
//                }
//            }
//        },
//        _getLotInfo(data) {
//            return rpc.query({
//                model: 'package.spliting.barcode',
//                method: 'search_read',
//                domain: [['barcode', '=', data.code]]
//            })
//        }
//
//    });
//
//    /*var _super_order = models.Order.prototype;
//    models.Order = models.Order.extend({
//        display_lot_popup: function () {
//            var self = this;
//            var order_line = self.get_selected_orderline();
//            var pack_lot_lines = order_line.compute_lot_lines();
//            if (order_line && self.pos.lot_id) {
//                var pack_line = _.values(pack_lot_lines._byId)[0];
//                pack_line.set_lot_name(self.pos.lot_id);
//                pack_lot_lines.remove_empty_model();
//                pack_lot_lines.set_quantity_by_lot();
//                order_line.trigger('change', order_line);
//            } else if (order_line) {
//                self.pos.gui.show_popup('packlotline', {
//                    'title': _t('Lot/Serial Number(s) Required'),
//                    'pack_lot_lines': pack_lot_lines,
//                    'order_line': order_line,
//                    'order': this,
//                });
//            }
//        },
//    });*/
//})
//;
