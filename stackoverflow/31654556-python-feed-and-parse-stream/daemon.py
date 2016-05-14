#!/usr/bin/env python
from __future__ import print_function
import sys
import math
import select, time

if len(sys.argv) != 2:
    print("Expects one argument for logfile name.", file=sys.stderr)
    exit(1)

import logging
logger = logging.getLogger("SquareRooter")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(sys.argv[1])
logger.addHandler(fh)

shouldEnd=False
while(not shouldEnd):
    if select.select([sys.stdin,],[],[],0.0)[0]:
        try:
            line=raw_input()
            logger.debug("%s received as input." % line)
            try:
                num=int(line)
                if num < 0:
                    print("No natural square root of %d" % num, file=sys.stderr)
                else:
                    print(math.sqrt(num))
                    sys.stdout.flush()
            except ValueError:
                print("Not a number.", file=sys.stderr)
        except EOFError:
            shouldEnd=True
            break
    else:
        time.sleep(0.1)
