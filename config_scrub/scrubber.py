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
    def __init__(self, matchers):
        if not isinstance(matchers, list):
            raise ScrubberException("matchers must be a list")

        if len(matchers) == 0:
            raise ScrubberException("No matchers present, no work to do")

        self.matchers = matchers

    def scrub_line(self, line):
        new_line = line
        for matcher in self.matchers:
            if isinstance(matcher, ScrubberMatcher):
                new_line = matcher.scrub(new_line)

        return new_line
