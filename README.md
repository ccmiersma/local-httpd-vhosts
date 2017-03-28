Local Software Distribution
===========================

This package will install the base environment for a custom software distribution.
This can serve as a starting point for a complete integrated set of scripts, configurations,
and custom applications local to your organization.

This sets up a software tree similar to /usr/ or /usr/local under /opt/local, or
the path of your choice. This allows packaged scripts to be easily distinguished
from the operating system and third-party vendors.

The configuration is added to the environment through 3 files:
1. A set of environmental variables in /etc/sysconfig/local
2. A library of bash functions in /opt/local/lib/scripts that uses variables defined in /etc/sysconfig/local
3. A config file in /etc/opt/local/base-sw-dist.conf that can override variables and functions. By default it activates the configuration by exporting the variables.

The files are sourced in that order by a profile script. The first and last files are config files that can 
extend the local installation without impacting updates to the library by future verisons.
