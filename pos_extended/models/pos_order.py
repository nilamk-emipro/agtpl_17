import json
from odoo import models, fields, api, _


class PosOrders(models.Model):
    _inherit = "pos.order"

    with_effort = fields.Boolean("With Effort")
    salesman_id = fields.Many2one(comodel_name='hr.employee', string="Salesman")

    @api.model
    def _order_fields(self, ui_order):
        order_fields = super(PosOrders, self)._order_fields(ui_order)
        config_id = order_fields['session_id'] and self.env['pos.session'].browse(
            order_fields['session_id']).config_id or self.env['pos.config']
        if not order_fields.get('fiscal_position_id', False) and config_id.fiscal_position_ids:
            fpos_ids = self.env['account.fiscal.position'].sudo().with_company(order_fields['company_id']).with_context(
                company_id=order_fields['company_id'], fpos=config_id.fiscal_position_ids).get_fiscal_position(
                order_fields['partner_id'])
            order_fields['fiscal_position_id'] = fpos_ids.id
        if not order_fields.get('with_effort', False) and not order_fields.get('salesman_id', False) and config_id.authorized_salesman_ids:
            order_fields['with_effort'] = ui_order.get('with_effort')
            order_fields['salesman_id'] = ui_order.get('salesman_id')
        return order_fields

    @api.model
    def get_ack_no_and_irn_no(self, receipt):
        data = {}
        if receipt:
            pos_order = self.search([('pos_reference', '=', receipt.get('name'))], limit=1)
            invoice = pos_order.account_move
            pos_partner_id = pos_order.session_id.config_id.warehouse_id.partner_id
            company_title = pos_partner_id.name
            company_street = pos_partner_id.street
            company_street2 = pos_partner_id.street2
            company_city = pos_partner_id.city
            company_state_id = pos_partner_id.state_id.name
            company_zip = pos_partner_id.zip
            company_country_id = pos_partner_id.country_id.name
            if invoice:
                data.update({'invoice_no': invoice.name, 'invoice_date': invoice.invoice_date.strftime("%d-%m-%Y"),
                             'session_id': pos_order.session_id.name, 'pos_order_id': pos_order.name,
                             'order_date': pos_order.date_order,
                             'company_title': company_title,
                             'company_street': company_street,
                             'company_street2': company_street2,
                             'company_city': company_city,
                             'company_state_id': company_state_id,
                             'company_zip': company_zip,
                             'company_country_id': company_country_id,

                             })
                documents = json.loads((invoice.edi_document_ids.filtered(lambda
                                                                              i: i.edi_format_id.code == 'in_einvoice_1_03' and i.attachment_id.mimetype == 'application/json').attachment_id.raw or b'{}').decode(
                    'utf-8'))
                if documents:
                    if documents.get('AckNo'):
                        data.update({'AckNo': documents.get('AckNo')})
                    if documents.get('Irn'):
                        data.update({'Irn': documents.get('Irn')})
                    if documents.get('SignedQRCode'):
                        data.update({'QrCode': documents.get('SignedQRCode')})
        return data

    @api.model
    def set_partner_warning(self, partner_data, screen):
        partner_id = self.env['res.partner'].browse(partner_data.get('id'))
        if not partner_id:
            return
        if partner_id and not partner_id.sale_warn or not partner_id.invoice_warn:
            return
        partner = partner_id
        partner_warn = partner.sale_warn if screen.get('product-screen') else partner.invoice_warn
        partner_warn_message = partner.sale_warn_msg if screen.get('product-screen') else partner.invoice_warn_msg

        # If partner has no warning, check its company
        if partner_warn == 'no-message' and partner.parent_id:
            partner = partner.parent_id

        if partner_warn and partner_warn != 'no-message':
            # Block if partner only has warning but parent company is blocked
            if partner_warn != 'block' and partner.parent_id and partner_warn == 'block':
                partner = partner.parent_id

            if partner_warn == 'block':
                partner_data = {}

            return {
                'warning': {
                    'title': _("Warning for %s", partner.name),
                    'message': partner_warn_message,
                    'partner_data': partner_data
                }
            }
