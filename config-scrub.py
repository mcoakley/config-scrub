#!/usr/bin/env python

import argparse
import os
import sys

from config_scrub.password_scrub import (
    build_password_matchers,
    load_passwords_from_file,
)
from config_scrub.scrubber import DEFAULT_REDACT_STRING, Scrubber
from config_scrub.loadable_scrubber import LoadableScrubber

DEFINITIONS_PATH = "./definitions"


def create_loadable_scrubber():
    scrubber = LoadableScrubber()

    try:
        (_, _, filenames) = next(os.walk(DEFINITIONS_PATH))
        for filename in filenames:
            scrubber.load_file(os.path.join(DEFINITIONS_PATH, filename))

        return scrubber
    except StopIteration:
        raise Exception("Could not load the RegEx definitions")


def main():
    parser = argparse.ArgumentParser(
        description="Scrub configuration files for passwords "
        + "and other private information"
    )
    parser.add_argument("--passfile", metavar="filepath")

    args = parser.parse_args()

    password_scrubber = None
    if args.passfile:
        passwords = load_passwords_from_file(args.passfile)
        password_matchers = build_password_matchers(
            passwords, DEFAULT_REDACT_STRING
        )
        password_scrubber = Scrubber(password_matchers)

    content_scrubber = create_loadable_scrubber()

    for line in sys.stdin:
        new_line = line.rstrip()
        if new_line != "":
            new_line = content_scrubber.scrub_line(new_line)
            if password_scrubber:
                new_line = password_scrubber.scrub_line(new_line)

        print(new_line)


if __name__ == "__main__":
    main()
