#!/usr/bin/env python

import sys

from config_scrub.unknown_scrub import UnknownScrubber

scrubber = UnknownScrubber()

for line in sys.stdin:
    print(scrubber.scrub_line(line.rstrip()))
