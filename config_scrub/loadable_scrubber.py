import re

from .scrubber import DEFAULT_REPLACER, Scrubber, ScrubberMatcher

# _SET_SNMP_COMMUNITY_MATCHER = r"^( *<data access.+community=\")(\S+)(\".+/>)"
# _SET_SNMP_TRAP_COMMUNITY_MATCHER = (
#     r"^( *<data community=\")(\S+)(\".+type=\"trap\".+/>)"
# )

REPLACEMENT_IDENTIFIER = "replacement:"

# We use the raw_map to convert interpreted RegEx positional markers back
# e.g. when we read a string from a file the raw string r'\1{REDACTED}\3'
#      will be converted to '\x01{REDACTED}\x03'
#
# See https://stackoverflow.com/a/21605790/7102037
RAW_MAP = {
    1: r"\1",
    2: r"\2",
    3: r"\3",
    4: r"\4",
    5: r"\5",
    6: r"\6",
    7: r"\7",
    8: r"\8",
    9: r"\9",
    10: r"\10",
}


class LoadableScrubber(Scrubber):
    # def __init__(self):
    #     my_matchers = [
    #         ScrubberMatcher(_SET_SNMP_COMMUNITY_MATCHER, DEFAULT_REPLACER),
    #         ScrubberMatcher(
    #             _SET_SNMP_TRAP_COMMUNITY_MATCHER, DEFAULT_REPLACER
    #         ),
    #     ]
    #     super().__init__(my_matchers)

    def load_file(self, filepath):
        matchers = []
        current_pattern = ""
        with open(filepath, encoding="utf8") as f:
            for line in f:
                line = line.rstrip()

                # Skip blank and comment lines
                if line == "" or line[0] == "#":
                    continue

                # Save our current line so we can see if we are being
                # provided a specific replacement
                if current_pattern == "":
                    current_pattern = re.compile(line)
                    continue

                # We have a current pattern so check if this line is a
                # specific replacement or we simply have a new pattern
                replacement_identifier_len = len(REPLACEMENT_IDENTIFIER)
                if (
                    line[:replacement_identifier_len]
                    != REPLACEMENT_IDENTIFIER
                ):
                    matchers.append(
                        ScrubberMatcher(current_pattern, DEFAULT_REPLACER)
                    )
                    current_pattern = re.compile(line)
                else:
                    replace_line = line[replacement_identifier_len:].lstrip(
                        " "
                    )
                    raw_line = r"".join(
                        i if ord(i) > 32 else RAW_MAP.get(ord(i), i)
                        for i in replace_line
                    )
                    matchers.append(
                        ScrubberMatcher(current_pattern, raw_line)
                    )
                    current_pattern = ""

        if current_pattern != "":
            matchers.append(
                ScrubberMatcher(current_pattern, DEFAULT_REPLACER)
            )

        self.add_matchers(matchers)
