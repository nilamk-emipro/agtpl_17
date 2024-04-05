odoo.define('pos_extended.SetSalesmanButton', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');

    class SetSalesmanButton extends PosComponent {
        constructor() {
            super(...arguments);
            useListener('click', this.onClick);
        }
        mounted() {
            this.env.pos.get('orders').on('add remove change', () => this.render(), this);
            this.env.pos.on('change:selectedOrder', () => this.render(), this);
        }
        willUnmount() {
            this.env.pos.get('orders').off('add remove change', null, this);
            this.env.pos.off('change:selectedOrder', null, this);
        }
        get currentOrder() {
            return this.env.pos.get_order();
        }
        get currentSelectedSalesmanName() {
            return this.env.pos.config.auth_salesman_selection && this.currentOrder && this.currentOrder.salesman_id
                ? this.currentOrder.salesman_id.display_name
                : this.env._t('Salesman');
        }
        async onClick() {
            const authorized_salesman = this.currentOrder.salesman_id;
            const salesmanList = [
                {
                    id: -1,
                    label: this.env._t('None'),
                    isSelected: !authorized_salesman,
                },
            ];
            for (let salesman of this.env.pos.authorizedSalesmans) {
                salesmanList.push({
                    id: salesman.id,
                    label: salesman.name,
                    isSelected: authorized_salesman
                        ? salesman.id === authorized_salesman.id
                        : false,
                    item: salesman,
                });
            }
            const { confirmed, payload: selectedSalesman } = await this.showPopup(
                'SelectionPopup',
                {
                    title: this.env._t('Select Salesman'),
                    list: salesmanList,
                }
            );
            if (confirmed) {
                this.currentOrder.salesman_id = selectedSalesman;
            }
        }

    }
    SetSalesmanButton.template = 'SetSalesmanButton';

    ProductScreen.addControlButton({
        component: SetSalesmanButton,
        condition: function() {
            return this.env.pos.config.authorized_salesman_ids.length > 0;
        },
        //position: ['after', 'SetSaleOrderButton'],
    });

    Registries.Component.add(SetSalesmanButton);

    return SetSalesmanButton;
});
