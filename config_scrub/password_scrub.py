import os.path

from .scrubber import ScrubberMatcher


class PasswordMatcher(ScrubberMatcher):
    def scrub(self, line):
        return line.replace(self.pattern, self.replacement)


class PasswordFileException(Exception):
    pass


def build_password_matchers(passwords, replacement):
    matchers = []
    for password in passwords:
        matchers.append(PasswordMatcher(password, replacement))

    return matchers


def load_passwords_from_file(file_path):
    if not os.path.isfile(file_path):
        raise PasswordFileException("Password file not found")

    with open(file_path) as f:
        content = f.readlines()

    passwords = []
    for line in content:
        passwords.append(line.rstrip())

    return passwords
