# Kairos
Vulnerability assesment tool for the web based on side-channel timing attacks.

## Requirements

[Python](https://www.python.org/downloads/) version > 3.6 or more

## Usage

```
python domain-finder.py [-h] [-i] [-l] [-c] [-n] [--version]
```
<b>Where: </b>

 -h, --help          show help message and exit
 
  -i, --input         Simple Lookup. Searches for availability of the
                      specified domain name. (.com and .net top-level domains
                      supported)
                      
  -l, --list-domains  Advanced search. This option takes in a list of space
                      separated strings, generates all possible (and best)
                      combinations between them, and then checks their
                      avalability as domain names via DNS lookup.
                      
  -c, --com           Filter results by .com domains only.
  
  -n, --net           Filter results by .net domains only.
  
  --version           show program's version number and exit
  
  
  ## See it in action