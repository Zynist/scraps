#!/usr/bin/env python
import os
import sys
thisdir = os.path.abspath(os.path.dirname(__file__))
parentdir = "/".join(thisdir.split('/')[:-1])
sys.path.insert(0, parentdir)

from lib import common
value = common.server_ip

print "IP is %s" % value
