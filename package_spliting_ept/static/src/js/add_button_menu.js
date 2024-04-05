/** @odoo-module **/

import MainMenu from "@stock_barcode/stock_barcode_menu";

MainMenu.include({
    events: Object.assign({}, MainMenu.prototype.events, {
        'click .button_package_spliting': '_onClickPackageSpliting',
    }),

    _onClickPackageSpliting: function () {
        this.do_action('package_spliting_ept.package_spliting_main_screen');
    },
});
