
# Appendix 


## 1.2 User Requirements

### ORDS Installer Privileges Script

#### About the script

> Note: This script is used when you do not want to use SYS AS SYSDBA to install, upgrade, repair, and uninstall ORDS for Oracle PDB or Oracle 11g.

A script file is included in each ORDS download package that provides privileges to a user for ORDS:

- install/uninstall
- upgrade
- repair

The Oracle REST Data Services contains a script, ords_installer_privileges.sql which is located in the scripts/installer folder. The script provides the assigned database user the privileges to install, upgrade, repair, and uninstall ORDS in Oracle Database.
Perform the following steps:

    Using SQLcl or SQL*Plus, connect to the Oracle Database instance. You must have a Database account with appropriate privileges for installing ORDS.
    Execute the following script providing the database user:

    SQL> @/path/to/scripts/installer/ords_installer_privileges.sql exampleuser
    SQL> exit

You must use the specified database user to install, upgrade, repair, and uninstall ORDS.

> [Return to the Guide](./1-ords-installation-checklist.md#1.2userrequirements)

#### Review Privileges

When the ORDS Installer Privileges script is used, a user is granted equal privileges to install, upgrade, repair, and uninstall ORDS for either/both:

- Oracle Pluggable Database<sup>1</sup>
- Oracle 11g 

<sup>1</sup>Learn about [PDBs](https://docs.oracle.com/en/database/oracle/oracle-database/21/cncpt/introduction-to-oracle-database.html#GUID-ED16D715-761B-4F8B-8503-BC058E216D2F)

> [Return to the Guide](./1-ords-installation-checklist.md#1.2userrequirements)


## 1.3 Command Line Tool


> [Return to the Guide](./1-ords-installation-checklist.md#1.2userrequirements)

## 2.1 Java EE Application Servers

### Tomcat 10 experimental settings


> [Return to the Guide](./1-ords-installation-checklist.md##1.2userrequirements)