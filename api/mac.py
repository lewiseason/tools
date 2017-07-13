import os
import re
from flask import jsonify, abort, render_template
from api import app

valid_mac_address = re.compile(r'^[0-9A-Z]{6,12}$')
datasource = os.environ.get('MAC_OUI_DATASOURCE',
                            '/usr/share/nmap/nmap-mac-prefixes')


@app.route('/mac/')
def help():
    return render_template('mac/help.html')


@app.route('/mac/<address>')
def info(address):
    try:
        oui, vendor = lookup_oui(sanitize_mac(address))
        return jsonify(oui=oui, vendor=vendor)
    except TypeError:
        return jsonify(), 404


def sanitize_mac(address):
    address = re.sub(r'[^0-9a-zA-Z]', '', address).upper()

    if valid_mac_address.match(address):
        return address


def lookup_oui(address):
    oui = address[0:6]
    matcher = re.compile(r'^%s ' % oui)

    with open(datasource) as fh:
        for line in fh:
            if matcher.match(line):
                return line.strip().split(' ', 1)
