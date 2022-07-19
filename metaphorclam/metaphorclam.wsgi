#!/usr/bin/env python3

import clam.clamservice
import metaphorclam.metaphorclam as service
application = clam.clamservice.run_wsgi(service)

