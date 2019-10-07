# NITK CAA
Auto auth into NITK captive portal on your linux box.

Installs a systemd service that maintains login and an executable for one-off logins.

## Install
```bash
Clone this repo

$ git clone https://github.com/srinskit/nitkcaa.git

Run install script

$ ./install.sh username password
```

## Uninstall
```bash
Run uninstall script

$ ./uninstall.sh
```

## One-off login
```bash
$ nitkcaa
```

## Options
```bash
$ nitkcaa -h
usage: nitkcaa [-h] [--service] [--verbose] [config_file]

positional arguments:
  config_file  Path to config file (usually ~/.nitkcaa.conf)

optional arguments:
  -h, --help   show this help message and exit
  --service    run in service mode
  --verbose    view more logs
```

## Notes
* Enclose `username` and `password` in quotes if they contain special chars. 
* Do not delete the clone.
* Use the optional 3rd param in `install.sh` to use a custom service unit path
* Config file is `~/.nitkcaa.conf` by default
