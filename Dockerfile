FROM lwinmgmg/odoo:17.0

COPY . /mnt/extra-addons/.

RUN pip install -r /mnt/extra-addons/requirements.txt

COPY entrypoint.sh /

ENTRYPOINT ["/entrypoint.sh"]

CMD [ "odoo" ]
