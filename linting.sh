#!/bin/bash
# Black Formatter
echo "ODOO_DIR=${ODOO_DIR:-../odoo17}"
echo "ADDON_DIR=${ADDON_DIR:-$(pwd)}"

echo "Black Formatter is running"
black .
echo "Done..."

# Flake8 Linter
echo "Flake8 Linter is running"
flake8
echo "Done..."


# Pylint Linter
echo "Pylint Linter is running"
pylint --rcfile=.pylintrc --init-hook="import sys; sys.path.append('${ODOO_DIR}')" ${ADDON_DIR}
echo "Done..."
