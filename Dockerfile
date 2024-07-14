FROM lwinmgmg/odoo:17.0

COPY . /mnt/extra-addons/.

RUN pip install -r /mnt/extra-addons/requirements.dev.txt

ENTRYPOINT ["/entrypoint.sh"]

RUN [ "odoo" ]
