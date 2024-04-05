# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
"""
One transient model for odoo that will Import Advance Shipping Note(ASN). ASN is either CSV or
XLSX file.
For Importing ASN operation we've created some functions and procedures for processing ASN.

@author : Haresh Mori on dated 08-November-2021
"""
import os
import base64
import csv
import logging
import time

import chardet
import xlrd

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

_logger = logging.getLogger(__name__)


class ImportAsnEpt(models.TransientModel):
    """
    Model used for Importing Advance Shipping Note(ASN).
    """
    _name = 'import.asn.ept'
    _description = 'Import Advance Shipping Note'

    import_document = fields.Binary(string='Import File',
                                    help='Import file that contains Advance Shipping note')
    document_name = fields.Char(help='Name of import file')
    picking_id = fields.Many2one('stock.picking', string='Picking')

    @api.model
    def default_get(self, fields_list):
        """
        To set default value in picking_id field.
        :param fields_list:
        :return: res
        @author : Haresh Mori on dated 08-November-2021
        """
        res = super(ImportAsnEpt, self).default_get(fields_list)
        if 'picking_id' in fields_list:
            res['picking_id'] = self._context.get('picking_id')
        return res

    def add_asn_lines(self):
        """
        Created for adding ASN lines to `stock.move.line` from CSV file,
        This method will read CSV file from `import_document` field and convert binary field to
        dictionary and after that create move_line_ids.
        @author: Haresh Mori @Emipro Technologies Pvt. Ltd on date 8 November 2021 .
        Task_id: 179613 - ASN functionality development
        """
        start_time = time.time()
        file_name = self.document_name
        _logger.info(_("Import Operation --- Start, File: {file},"
                       "Time {start_time}".format(start_time=start_time, file=file_name)))

        data = self.check_file_extension_and_prepare_data()

        picking_list = []
        data_lines = list(data)
        for count, row in enumerate(data_lines):
            _logger.info("Processing Line: {} out of {}".format(count + 1, len(data_lines)))
            _logger.info("Line: {} ".format(row))

            row_values, error_msg, mismatch_row_data = self.check_file_values(row)
            existing_data = self.check_file_values_with_odoo_data(row_values, error_msg, mismatch_row_data)
            self.picking_validation(existing_data, error_msg)
            self.move_validation(row_values, existing_data, error_msg)
            self.update_move_lines(row, row_values, existing_data)

            picking_id = existing_data.get('picking_id')
            if not picking_id in picking_list:
                picking_list.append(picking_id)

        _logger.info(_("Import Operation --- End, Total Execution Time: {}".format(
            time.time() - start_time)))

        self.validate_pickings(picking_list)

    def check_file_extension_and_prepare_data(self):
        """
        This method is used to check the file extension. It will allow only .csv or .xlsx file format.
        @author: Haresh Mori @Emipro Technologies Pvt. Ltd on date 8 November 2021 .
        Task_id: 179613 - ASN functionality development
        @return: Data: Prepare data according to file extension.
        """
        data = ''
        try:
            name, ext = os.path.splitext(self.document_name)
        except ImportError as error:
            _logger.error(error)
        if ext in ('.csv', '.xlsx'):
            method = "_read_{}_file".format(ext.strip('.'))
            if hasattr(self, method):
                data = getattr(self, method)(self.import_document)
        else:
            raise ValidationError(
                _('Please provide only .csv or .xlsx file format to import ASN!!!'))
        return data

    def _read_csv_file(self, import_document):
        """
        This method is used to read and prepare data from imported CSV file.
        @param import_document: Imported file from the wizard.
        @return reader: Data
        @author: Haresh Mori @Emipro Technologies Pvt. Ltd on date 9 November 2021 .
        Task_id: 179613 - ASN functionality development
        """
        b64decode = base64.b64decode(import_document)
        encoding = chardet.detect(b64decode)['encoding'].lower()
        if encoding != 'utf-8':
            data = b64decode.decode(encoding).encode('utf-8')
            lines = data.splitlines()
            lines = [line.decode('utf-8') for line in lines]
        else:
            data = b64decode.decode('utf-8')
            lines = data.splitlines()
        # Need to Convert to List because of bytes
        reader = csv.DictReader(lines, delimiter=',')
        self.check_header_name(reader.fieldnames)
        return reader

    def _read_xlsx_file(self, import_document):
        """
        This method is used to read and prepare data from imported XLSX file.
        @param import_document: Imported file from the wizard.
        @return reader: list of dictionary of file data.
        @author: Haresh Mori @Emipro Technologies Pvt. Ltd on date 9 November 2021 .
        Task_id: 179613 - ASN functionality development
        """
        # Worksheet
        xl_workbook = xlrd.open_workbook(file_contents=base64.decodebytes(import_document))
        worksheet = xl_workbook.sheet_by_index(0)

        # Column  Header
        column_header = {}
        for col_index in range(worksheet.ncols):
            value = worksheet.cell(0, col_index).value.lower()
            column_header.update({col_index: value})
        headers = worksheet.row_values(0)
        self.check_header_name(headers)
        # File Data
        data_list = []
        for row_index in range(1, worksheet.nrows):
            sheet_data = {}
            for col_index in range(worksheet.ncols):
                sheet_data.update({
                    column_header.get(col_index): worksheet.cell(row_index, col_index).value or ''})
            if bool(sheet_data):
                data_list.append(sheet_data)

        return data_list

    def check_header_name(self, headers=[]):
        """
        This method is used to check the validation of header name.
        @author: Haresh Mori @Emipro Technologies Pvt. Ltd on date 9 November 2021 .
        Task_id: 179613 - ASN functionality development
        """
        default_header_list = ['internal_default_code', 'vendor_default_code', 'package', 'expected_qty', 'po_number',
                               'uom']
        for header_name in headers:
            if header_name not in default_header_list:
                error_message = "Please Give Proper Header Name in file!!!\n" \
                                "Valid Header Names:\n\n" \
                                "{list}".format(list=',\n'.join(default_header_list))
                raise ValidationError(error_message)

    def check_file_values(self, row):
        """
        This method is used to check the values of the CSV file. It will raise the warning message if values are not
        proper or incorrect.
        @return row_values: It return the row values in the dictionary.
        @return line:  Row values to use in the warning message.
        @row: Row of file.
        @author: Haresh Mori @Emipro Technologies Pvt. Ltd on date 9 November 2021 .
        Task_id: 179613 - ASN functionality development
        """
        row_values = {}
        try:
            po_number = row.get('po_number', '')
            internal_default_code = row.get('internal_default_code', '')
            vendor_default_code = row.get('vendor_default_code', '')
            # internal_lot = row.get('internal_lot', '')
            # vendor_lot = row.get('vendor_lot', '')
            expected_qty = row.get('expected_qty', '')
            uom = row.get('uom', '')
        except Exception as e:
            _logger.exception("File Line Read Exception: {}".format(e))
            raise ValidationError(_("File Line Read Exception: {}".format(e)))

        error_msg = "Purchase Order Reference: {ref}\nError:\n" \
                    "- ".format(ref=po_number) if po_number else ''
        line = "Line Data: \n" \
               "Purchase Order: {po}\n" \
               "Internal Default Code: {internal_sku}\n" \
               "Vendor Default Code: {vendor_sku}\n" \
               "Expected Qty: {expected_qty}\n".format(po=po_number,
                                                       internal_sku=internal_default_code,
                                                       vendor_sku=vendor_default_code,
                                                       expected_qty=expected_qty)
        # Validation: File content is properly filled or not.
        if not po_number:
            raise ValidationError(_('Please provide the `PO Number` in file\n'
                                    ' For File Line: {line}'.format(line=line)))

        if not (internal_default_code or vendor_default_code):
            raise ValidationError(_(error_msg + 'Please provide the `Product Code` '
                                                'or `Vendor Product '
                                                'Code` in file\n ' + line))
        # if not (internal_lot or vendor_lot):
        #     raise ValidationError(_(error_msg + 'Please provide `Vendor Lot` '
        #                                         'or `Internal Lot` in file\n' + line))
        try:
            expected_qty = float(expected_qty)
        except Exception as e:
            raise ValidationError(_(error_msg + 'Please provide expected quantity in digit '
                                                'only.\n' + line))
        row_values.update({'po_number': po_number, 'internal_default_code': internal_default_code,
                           'vendor_default_code': vendor_default_code, 'expected_qty': expected_qty, 'uom': uom})
        return row_values, error_msg, line

    def check_file_values_with_odoo_data(self, row_values, error_msg, mismatch_row_data):
        """
        In this method, the row values are checked against the Odoo data, like if the purchase order or product
        exists in Odoo or not. The warning message will be displayed if the required data does not exist in Odoo.
        @return : It will return the dictionary with Odoo existing data.
        @author: Haresh Mori @Emipro Technologies Pvt. Ltd on date 9 November 2021 .
        Task_id: 179613 - ASN functionality development
        """
        purchase_obj = self.env['purchase.order']
        product_obj = self.env['product.product']
        supplierinfo_obj = self.env['product.supplierinfo']
        uom_obj = self.env['uom.uom']
        po_number = row_values.get('po_number')
        default_code = row_values.get('internal_default_code')
        vendor_default_code = row_values.get('vendor_default_code')
        uom = row_values.get('uom')
        purchase_order = purchase_obj.search([('name', '=', po_number.strip())], limit=1)
        existing_data = {}
        if not purchase_order:
            raise ValidationError("Purchase order not found for the order reference "
                                  "`{order}`.".format(order=po_number))
        existing_data.update(
            {'purchase_order': purchase_order, 'supplier_short_code': purchase_order.partner_id.name_short_code or ''})

        if default_code:
            product_id = product_obj.search([('default_code', '=', default_code)])
            if product_id and len(product_id) > 1:
                raise UserError(_(error_msg + 'There is multiple product with Internal reference:'
                                              ' {internal_sku}'.format(internal_sku=default_code)))
            elif not product_id:
                raise UserError(_(error_msg + 'Product not found for Internal reference: ' '{internal_sku} \n'.format(
                    internal_sku=default_code) + mismatch_row_data))
            existing_data.update({'product_id': product_id})
        else:
            supplier = supplierinfo_obj.search([('product_code', '=', vendor_default_code)], limit=1)

            if supplier:
                product_id = supplier.product_id or supplier.product_tmpl_id.product_variant_id
                existing_data.update({'supplier_product_code': supplier.product_code})

                if product_id and len(product_id) > 1:
                    raise UserError(
                        _(error_msg + 'There is multiple product with Vendor Internal reference: {vendor_sku}'.format(
                            vendor_sku=vendor_default_code)))
                elif not product_id:
                    raise UserError(
                        _(error_msg + 'Product not found for Vendor Internal reference: {vendor_sku}'.format(
                            vendor_sku=vendor_default_code)))
                existing_data.update({'product_id': product_id, 'supplier': supplier})
            else:
                raise UserError(
                    _(error_msg + 'Product not found for Vendor Internal reference: {vendor_sku}'.format(
                        vendor_sku=vendor_default_code)))
        if uom:
            uom_id = uom_obj.search([('name', '=', uom)], limit=1)
            if uom_id:
                existing_data.update({'uom': uom_id})
        return existing_data

    def picking_validation(self, existing_data, error_msg):
        """
        This method is used to check the picking validation.
        @author: Haresh Mori @Emipro Technologies Pvt. Ltd on date 9 November 2021 .
        Task_id: 179613 - ASN functionality development
        """
        purchase_order = existing_data.get('purchase_order')
        picking_id = purchase_order.picking_ids.filtered(lambda x: x.state in ['assigned'])

        _logger.info("Processing Picking ----- {}".format(picking_id))

        if picking_id and len(picking_id) > 1:
            raise ValidationError(_(error_msg + "\n" + 'Multiple Picking found.'))
        elif not picking_id:
            raise ValidationError(_(error_msg + "\n" + 'Picking not found.'))

        # If import_asn_flag is set true then it will reset all the imports and False the flag and re-import.
        if picking_id.import_asn_flag:
            _logger.info("Picking--{}, Reset move line if any of the ASN imported by mistake".format(picking_id))
            try:
                picking_id.button_reset_asn()
            except Exception as e:
                raise ValidationError(_("Reset Move Lines Exception Occurred: {}".format(e)))
        existing_data.update({'picking_id': picking_id})

    def move_validation(self, row_values, existing_data, error_msg):
        """
        This method is used to check the move validation.
        @author: Haresh Mori @Emipro Technologies Pvt. Ltd on date 9 November 2021 .
        Task_id: 179613 - ASN functionality development
        """
        # Moves with same product
        production_lot_obj = self.env['stock.production.lot']
        picking_id = existing_data.get('picking_id')
        product_id = existing_data.get('product_id')
        supplier_product_code = existing_data.get('supplier_product_code')
        supplier_short_code = existing_data.get('supplier_short_code')
        # internal_lot = row_values.get('internal_lot')
        # vendor_lot = row_values.get('vendor_lot')
        move_id = picking_id.move_ids_without_package.filtered(lambda m: m.product_id.id == product_id.id)

        if not move_id:
            move_msg = 'Product move not found for internal reference : {} in picking: {}'.format(
                product_id.default_code or supplier_product_code, picking_id.name)
            raise ValidationError(_(error_msg + move_msg))

        # if internal_lot and move_id.product_id.tracking == 'none':
        #     raise ValidationError(_(error_msg + 'CSV contains lot but lot is not enabled in product: {}.'.format(
        #         move_id.product_id.default_code)))

        if len(move_id) > 1:
            raise ValidationError(_(error_msg + 'Transfer: {}, '
                                                'Multiple moves found for product : {}'.format(picking_id.name,
                                                                                               move_id.mapped(
                                                                                                   'product_id').display_name)))

        # vendor_lot = supplier_short_code + vendor_lot if vendor_lot else ''
        # # Lots Prepare: Preparing the domain for searching the lot.
        # if internal_lot:
        #     domain = [('product_id', '=', product_id.id),
        #               ('name', '=', internal_lot)]
        # else:
        #     domain = [('product_id', '=', product_id.id),
        #               ('ref', '=', vendor_lot)]
        # Find: Lot as per the domain
        # lot_id = production_lot_obj.search(domain)

        # Move Lines
        # Find: Move-lines with lot, either internal lot or vendor lot.
        # move_line_ids = move_id.move_line_ids.filtered(
        #     lambda ml: (ml.lot_name == internal_lot) or (ml.lot_id.ref and ml.lot_id.ref == vendor_lot))
        move_line_ids = move_id.move_line_ids
        existing_data.update({'move_line_ids': move_line_ids, 'move_id': move_id})

    def update_move_lines(self, row, row_values, existing_data):
        """
        This method is used to create/update the move line.
        @param row: Values of row.
        @param row_values: formatted values of row.
        @param existing_data: Dictionary of existing records.
        @author: Haresh Mori @Emipro Technologies Pvt. Ltd on date 9 November 2021 .
        Task_id: 179613 - ASN functionality development
        """
        move_line_ids = existing_data.get('existing_data')
        picking_id = existing_data.get('picking_id')
        # internal_lot = row_values.get('internal_lot')
        # vendor_lot = row_values.get('vendor_lot')
        product_id = existing_data.get('product_id')
        move_id = existing_data.get('move_id')
        # lot_id = existing_data.get('lot_id')
        expected_qty = row_values.get('expected_qty')
        package_uom = existing_data.get('uom')
        if not move_line_ids or (move_line_ids and not picking_id.import_asn_flag):
            package_id = self.create_package_lot(row, picking_id, product_id)
            # Append line on wizard
            if move_id:
                try:
                    vals = self.prepare_move_line_vals(move_id, package_id, expected_qty, picking_id)
                    if package_uom:
                        vals.update({'product_uom_id': package_uom.id})
                    move_id.move_line_ids = [(0, 0, vals)]
                    package_id.write({'is_assigned': True})
                except Exception as e:
                    raise ValidationError(
                        _("Transfer: {}, Update Move Line Exception : {}".format(picking_id._name, e)))

        elif picking_id.import_asn_flag:
            if move_line_ids:
                # Update existing line on move line wizard.
                try:
                    move_line_ids[0].write({
                        'expected_qty': float(expected_qty),
                        'product_uom_qty': float(expected_qty),
                    })
                except Exception as e:
                    _logger.exception("Transfer: {}, Updating Move Line "
                                      "Exception: {}".format(picking_id._name, e))
                    raise ValidationError(_("Transfer: {}, Updating Move Line "
                                            "Exception: {}".format(picking_id._name, e)))
            elif len(move_line_ids) > 1:
                raise ValidationError(_('Duplicate Move Line found for transfer: {}'.format(
                    picking_id.name)))

        # Remove unnecessary lines and maintain the `stock.quant`.
        for move_id in picking_id.move_lines:
            try:
                move_id.move_line_ids.filtered(
                    lambda x: x.product_uom_qty and not x.expected_qty).unlink()
            except Exception as e:
                _logger.exception("Transfer: {}, Move Line Delete Exception: {}".format(
                    picking_id._name, e))
                raise ValidationError(_("Transfer: {}, Exception: {}".format(
                    picking_id._name, e)))

    def create_package_lot(self, row, picking_id, product_id):
        """
        This method is used to create lot and package.
        @author: Haresh Mori @Emipro Technologies Pvt. Ltd on date 9 November 2021 .
        Task_id: 179613 - ASN functionality development
        """
        quant_package_obj = self.env['stock.quant.package']
        stock_production_lot = self.env['stock.production.lot']
        vals = {}
        if row.get('package', False):
            vals['name'] = row.get('package')
        try:
            package_id = quant_package_obj.with_context(is_asn_package=True).create(vals)
        except Exception as e:
            raise ValidationError("Transfer: {}, Package Creation Exception: {}".format(picking_id._name, e))

        # Create lot if not exists!
        # if not lot_id:
        # if internal_lot:
        #     lot_name = internal_lot
        # else:
        # lot_name = lot_id.env['ir.sequence'].next_by_code('stock.lot.serial')
        # try:
        #     lot_id = stock_production_lot.create({
        #         'name': lot_name,
        #         'product_id': product_id.id,
        #         'company_id': self.env.company.id
        #     })
        # except Exception as e:
        #     raise ValidationError("Transfer: {}, Lot Creation Exception: {}".format(picking_id._name, e))
        return package_id

    def prepare_move_line_vals(self, move_id, package_id, expected_qty, picking_id):
        """
        This method is use to prepare a move line vals.
        @return: Vals
        @author: Haresh Mori @Emipro Technologies Pvt. Ltd on date 9 November 2021 .
        Task_id: 179613 - ASN functionality development
        """
        vals = {
            'move_id': move_id.id,
            'result_package_id': package_id.id,
            # 'lot_id': lot_id.id,
            # 'lot_name': lot_id.name,
            'product_id': move_id.product_id.id,
            'product_uom_id': move_id.product_uom.id,
            'location_dest_id': move_id.location_dest_id.id,
            'location_id': move_id.location_id.id,
            'expected_qty': float(expected_qty),
            'product_uom_qty': float(expected_qty),
            'picking_id': picking_id.id,
            'qty_done': float(expected_qty),
        }
        return vals

    def validate_pickings(self, picking_list):
        """
        This method is use to validate the pickings.
        @author: Haresh Mori @Emipro Technologies Pvt. Ltd on date 9 November 2021 .
        Task_id: 179613 - ASN functionality development
        """
        validate_st_time = time.time()
        _logger.info("ALL Picking Action Assign Process - - - - Start, Time: {}".format(validate_st_time))
        _logger.info("Total Picking to Action Assign: {}, {}".format(len(picking_list), picking_list))
        for picking_id in picking_list:
            # Flag for visible and invisible reset button
            picking_id.import_asn_flag = True
            # We've removed some unnecessary move lines so we need to again call
            # action_assign() to maintain the stock.quant.
            if picking_id.show_check_availability:
                try:
                    picking_id.action_assign()
                except Exception as error:
                    raise ValidationError(
                        _("Transfer: {}, Action Assign Exception: {}".format(picking_id._name, error)))
            try:
                picking_id.with_context(imported_picking=True).button_validate()
            except Exception as error:
                raise ValidationError(_("Transfer: {}, Action Validate Exception: {}".format(picking_id._name, error)))
        _logger.info("ALL Picking Action Assign and Validation Process - - - - End, "
                     "Time: {}".format(time.time() - validate_st_time))
