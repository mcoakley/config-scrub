from .scrubber import DEFAULT_REPLACER, Scrubber, ScrubberMatcher


_SET_SNMP_COMMUNITY_MATCHER = r"^( *<data access.+community=\")(\S+)(\".+/>)"
_SET_SNMP_TRAP_COMMUNITY_MATCHER = (
    r"^( *<data community=\")(\S+)(\".+type=\"trap\".+/>)"
)


class UnknownScrubber(Scrubber):
    def __init__(self):
        my_matchers = [
            ScrubberMatcher(_SET_SNMP_COMMUNITY_MATCHER, DEFAULT_REPLACER),
            ScrubberMatcher(_SET_SNMP_TRAP_COMMUNITY_MATCHER, DEFAULT_REPLACER),
        ]
        super().__init__(my_matchers)
