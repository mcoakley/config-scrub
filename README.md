# config-scrub

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

This Python script will scrub a given configuration file for known elements that wish to be protected.

## Installation

```bash
git clone https://github.com/mcoakley/config-scrub
cd config-scrub
```

## Usage

> These examples assume you are in the folder where config-scrub.py exists, have setup a path to the file, or have copied the file to a location in your path.

On all platforms the `config-scrub.py` command supports the following command line parameters:

- `[-h | --help]` - returns a command help screen (optional)
- `[--passfile filepath]` - allows you to specify a password file that will be used to scrub the configuration file (optional)

### Password File

The `config-scrub.py` script can use a password file to look for known passwords in your configuration scripts and remove them. The password file is a normal text file that has a single password per line in the file.

```text
!password123
1amg0d
supp3r_s3cr%t_p@$$w0rd
```

### Unix / Linux Usage

```bash
./config-scrub.py < input-file.txt > output-file.txt
```

### Windows / PowerShell Usage

```powershell
type input-file.txt | .\config-scrub.py > output-file.txt
```

## Scrubbing Definitions

There is a `definitions` folder in the repository. Any file in this folder will be loaded at runtime and is expected to provide regular expression lines that will be used to match lines found in the files being scrubbed.

The `matcher` RegEx lines follow standard Python RegEx rules as per the `re` definition found [here](https://docs.python.org/3/library/re.html) (_NOTE: make sure you match the `re` documentation to your Python version._)

You can also define a `replacement` string on the line following the `matcher` line. The `replacement` string again follows standard Python RegEx practices. The `replacement` line **MUST** be prefaced with `replacement:` in order to properly be identified. A default `replacement` string will be used if you do not supply one.

**Default Replacement String**: `r'\1' + DEFAULT_REDACTED_STRING + r'\3'` where the `DEFAULT_REDACTED_STRING` is `{REDACTED}`.

### Examples

`misc.scrub`

```text
# XML file data

# XML community structure, redacting the community string
^( *<data access.+community=\")(\S+)(\".+/>)

# XML trap structure, redacting the community string
^( *<data community=\")(\S+)(\".+type=\"trap\".+/>)
```

> Blank lines and lines that start with a `#` will be ignored

In the above examples the default replacement string will be used.

So given the following data:

```xml
<snmp_community>
  <data access="read-only" address="1.1.1.1" community="my_secret_community_1" mask="255.255.255.255"/>
  <data access="read-only" address="2.2.2.2" community="my_secret_community_2" mask="255.255.255.255"/>
  <data access="read-only" address="3.3.3.3" community="my_secret_community_3" mask="255.255.255.255"/>
  <data access="read-only" address="4.4.4.4" community="my_secret_community_4" mask="255.255.255.255"/>
</snmp_community>
```

The scrubbed output will be:

```xml
<snmp_community>
  <data access="read-only" address="1.1.1.1" community="{REDACTED}" mask="255.255.255.255"/>
  <data access="read-only" address="2.2.2.2" community="{REDACTED}" mask="255.255.255.255"/>
  <data access="read-only" address="3.3.3.3" community="{REDACTED}" mask="255.255.255.255"/>
  <data access="read-only" address="4.4.4.4" community="{REDACTED}" mask="255.255.255.255"/>
</snmp_community>
```

Let's say we also wanted to redact the IP address, we would need a new matcher and a specific replacement.

Here is the definition file:

```text
# XML file data

# XML community structure, redacting the IP address and community string
^( *<data access.+address=\")(\S+)(\".+community=\")(\S+)(\".+/>)
replacement: \1x.x.x.x\3{REDACTED}\5
```

The scrubbed output will be:

```xml
<snmp_community>
  <data access="read-only" address="x.x.x.x" community="{REDACTED}" mask="255.255.255.255"/>
  <data access="read-only" address="x.x.x.x" community="{REDACTED}" mask="255.255.255.255"/>
  <data access="read-only" address="x.x.x.x" community="{REDACTED}" mask="255.255.255.255"/>
  <data access="read-only" address="x.x.x.x" community="{REDACTED}" mask="255.255.255.255"/>
</snmp_community>
```
