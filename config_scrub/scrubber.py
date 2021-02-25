import re

DEFAULT_REDACT_STRING = "{REDACTED}"
DEFAULT_REPLACER = r"\1" + DEFAULT_REDACT_STRING + r"\3"


class ScrubberMatcher:
    def __init__(self, pattern, replacement):
        self.pattern = pattern
        self.replacement = replacement

    def scrub(self, line):
        return re.sub(self.pattern, self.replacement, line)


class ScrubberException(Exception):
    pass


class Scrubber(object):
    def __init__(self, matchers=None):
        self.matchers = []
        self.add_matchers(matchers)

    def add_matchers(self, matchers):
        # We simply ignore an empty matchers
        if matchers is None:
            return

        if not isinstance(matchers, list):
            raise ScrubberException("matchers must be a list")

        valid_matchers = []
        for matcher in matchers:
            if isinstance(matcher, ScrubberMatcher):
                valid_matchers.append(matcher)

        self.matchers.extend(valid_matchers)

    def scrub_line(self, line):
        new_line = line
        for matcher in self.matchers:
            new_line = matcher.scrub(new_line)

        return new_line
