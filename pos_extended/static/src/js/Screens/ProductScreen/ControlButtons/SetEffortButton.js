odoo.define('pos_extended.SetEffortButton', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');

    class SetEffortButton extends PosComponent {
        constructor() {
            super(...arguments);
        }

        get currentOrder() {
            return this.env.pos.get_order();
        }

        toggleWithEffort() {
            this.currentOrder.set_effort(!this.currentOrder.is_effort());
            this.render();
        }
    }

    SetEffortButton.template = 'SetEffortButton';

    ProductScreen.addControlButton({
        component: SetEffortButton,
        condition: function() {
            return this.env.pos.config.auth_salesman_selection && this.env.pos.config.authorized_salesman_ids.length > 0;
        },
        //position: ['after', 'SetSaleOrderButton'],
    });

    Registries.Component.add(SetEffortButton);

    return SetEffortButton;
});
