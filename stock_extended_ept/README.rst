=====================
Stock Extended Ept
=====================

- This module will add one field in stock.move and stock.move.line and the field name is ``expected_qty``.

========
Features
========
- Import CSV of Advance Shipping Note (ASN) from Menu
    - It will open one wizard and in that wizard user can upload csv file for importing ASN lines in stock move line.
    - User can add one or more CSV file to import Advance Shipping Note (ASN).
    - User can reset Advance shipping note (ASN) if wrong file would be imported.
- File format changed and not checking package at the time of importing because it will only create the packages when move line generated.
- Puts onchange event when package is changing manually and if the package is assigned to different product.

=============================================
Validation For Import File
=============================================
- Provide `PO number` in file.
- Provide the `Product Code` or `Vendor Product Code` in file.
- Provide `Vendor Lot` or `Internal Lot` in file'.
- Provide expected quantity in file.
