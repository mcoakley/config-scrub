# config-scrub

This Python script will scrub a given configuration file for known elements that wish to be protected.

## Installation

```bash
git clone https://github.com/mcoakley/config-scrub
cd config-scrub
```

## Usage

> These examples assume you are in the folder where config-scrub.py exists, have setup a path to the file, or have copied the file to a pathed location.

### Unix/Linux Usage

```bash
./config-scrub.py < input-file.txt > output-file.txt
```

### Windows/PowerShell Usage

```powershell
type input-file.txt | .\config-scrub.py > output-file.txt
```
