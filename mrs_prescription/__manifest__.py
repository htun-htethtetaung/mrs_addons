# pylint: disable=pointless-statement,missing-module-docstring,duplicate-code
{
    "name": "Medical Record System Prescription",
    "version": "1.0.0",
    "category": "medical",
    "summary": "Medical Record System Prescription",
    "sequence": "1",
    "website": "https://www.cosmosmm.com",
    "author": "Lwin Maung Maung",
    "maintainer": "lwinmaungmaung@cosmosmm.com",
    "license": "LGPL-3",
    "description": "Medical Record System Prescription",
    "support": "lwinmaungmaung@cosmosmm.com",
    "depends": ["mrs_mrs"],
    "demo": [],
    "data": [
        "security/ir.model.access.csv",
        "views/prescription_order_view.xml",
        "views/visit_prescription_view.xml",
    ],
    "application": True,
    "installable": True,
}
