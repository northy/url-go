#!/usr/bin/env pipenv-shebang
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/PATH/TO/APP/")

from url_go import create_app
application = create_app()