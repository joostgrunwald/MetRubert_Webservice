#!/usr/bin/env python3

import clam.clamservice
import alpino_webservice.metaphorclam as service
application = clam.clamservice.run_wsgi(service)

