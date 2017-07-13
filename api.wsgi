import os
import sys

keep_env = ['MAC_OUI_DATASOURCE']

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

def application(environ, start_response):
    for var in keep_env:
        print(environ.get(var, ''))
        os.environ[var] = environ.get(var, '')

    from api import app as _application
    return _application(environ, start_response)
