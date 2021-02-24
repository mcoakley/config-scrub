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
