# pylint: disable=pointless-statement,missing-module-docstring
{
    "name": "Doctor",
    "version": "1.0.0",
    "category": "medical",
    "summary": "Doctor Module",
    "description": "Doctor Module",
    "sequence": "2",
    "website": "https://www.cosmosmm.com",
    "author": "Lwin Maung Maung",
    "maintainer": "lwinmaungmaung@cosmosmm.com",
    "support": "lwinmaungmaung@cosmosmm.com",
    "license": "LGPL-3",
    "depends": ["base", "mail", "contacts"],
    "demo": [],
    "data": [
        "security/ir.model.access.csv",
        "views/speciality_view.xml",
        "views/academic_view.xml",
        "views/professional_view.xml",
        "views/doctor_view.xml",
    ],
    "application": True,
    "installable": True,
}
