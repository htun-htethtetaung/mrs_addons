# pylint: disable=pointless-statement,missing-module-docstring,duplicate-code
{
    "name": "Medical Record System Program",
    "version": "1.0.0",
    "category": "medical",
    "summary": "Medical Record System Program",
    "description": "Medical Record System Program",
    "sequence": "1",
    "website": "https://www.cosmosmm.com",
    "author": "Lwin Maung Maung",
    "maintainer": "lwinmaungmaung@cosmosmm.com",
    "license": "LGPL-3",
    "support": "lwinmaungmaung@cosmosmm.com",
    "depends": ["mrs_mrs"],
    "demo": [],
    "data": [
        "security/ir.model.access.csv",
        "views/program_view.xml",
        "views/menus.xml",
        "views/visit_view.xml",
    ],
    "application": True,
    "installable": True,
}
