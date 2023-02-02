# Appendix 
## 2.1 Java EE Application Servers
Oracle REST Data Services supports Java EE application servers:

| Application Server | Supported Releases |
| --- | --- | 
|Oracle WebLogic Server | 14c or later | 
| Apache Tomcat | 8.5.x - 9.0.x | 

> Note: Tomcat Release 10 (in current docs says no, is that true?)

## 2.2 Oracle Application Express (APEX)

Oracle REST Data Services supports the currently supported versions of APEX. 

Can we just use this [link](https://www.oracle.com/us/assets/lifetime-support-technology-069183.pdf#%5B%7B%22num%22%3A154%2C%22gen%22%3A0%7D%2C%7B%22name%22%3A%22Fit%22%7D%5D)?

## 1.3 Prerequisites



### 1.3.2 

### 1.3.1 
## 1.3 Downloading ORDS



# Appendix 

## 2.1 Java EE Application Servers
Oracle REST Data Services supports Java EE application servers:

| Application Server | Supported Releases |
| --- | --- | 
|Oracle WebLogic Server | 14c or later | 
| Apache Tomcat | 8.5.x - 9.0.x | 

> Note: Tomcat Release 10 (in current docs says no, is that true?)

## 2.2 Oracle Application Express (APEX)

Oracle REST Data Services supports the currently supported versions of APEX. 

Can we just use this [link](https://www.oracle.com/us/assets/lifetime-support-technology-069183.pdf#%5B%7B%22num%22%3A154%2C%22gen%22%3A0%7D%2C%7B%22name%22%3A%22Fit%22%7D%5D)?

## 1.3 Prerequisites



### 1.3.2 

### 1.3.1 
## 1.3 Downloading ORDS



# Appendix 

## 2.1 Java EE Application Servers
Oracle REST Data Services supports Java EE application servers:

| Application Server | Supported Releases |
| --- | --- | 
|Oracle WebLogic Server | 14c or later | 
| Apache Tomcat | 8.5.x - 9.0.x | 

> Note: Tomcat Release 10 (in current docs says no, is that true?)

## 2.2 Oracle Application Express (APEX)

Oracle REST Data Services supports the currently supported versions of APEX. 

Can we just use this [link](https://www.oracle.com/us/assets/lifetime-support-technology-069183.pdf#%5B%7B%22num%22%3A154%2C%22gen%22%3A0%7D%2C%7B%22name%22%3A%22Fit%22%7D%5D)?

## 1.3 Prerequisites



### 1.3.2 

### 1.3.1 
## 1.3 Downloading ORDS



# Appendix 

## 2.1 Java EE Application Servers
Oracle REST Data Services supports Java EE application servers:

| Application Server | Supported Releases |
| --- | --- | 
|Oracle WebLogic Server | 14c or later | 
| Apache Tomcat | 8.5.x - 9.0.x | 

> Note: Tomcat Release 10 (in current docs says no, is that true?)

## 2.2 Oracle Application Express (APEX)

Oracle REST Data Services supports the currently supported versions of APEX. 

Can we just use this [link](https://www.oracle.com/us/assets/lifetime-support-technology-069183.pdf#%5B%7B%22num%22%3A154%2C%22gen%22%3A0%7D%2C%7B%22name%22%3A%22Fit%22%7D%5D)?

## 1.3 Prerequisites



### 1.3.2 

### 1.3.1 
## 1.3 Downloading ORDS



# Appendix 

## 2.1 Java EE Application Servers
Oracle REST Data Services supports Java EE application servers:

| Application Server | Supported Releases |
| --- | --- | 
|Oracle WebLogic Server | 14c or later | 
| Apache Tomcat | 8.5.x - 9.0.x | 

> Note: Tomcat Release 10 (in current docs says no, is that true?)

## 2.2 Oracle Application Express (APEX)

Oracle REST Data Services supports the currently supported versions of APEX. 

Can we just use this [link](https://www.oracle.com/us/assets/lifetime-support-technology-069183.pdf#%5B%7B%22num%22%3A154%2C%22gen%22%3A0%7D%2C%7B%22name%22%3A%22Fit%22%7D%5D)?

## 1.3 Prerequisites



### 1.3.2 

### 1.3.1 
## 1.3 Downloading ORDS



# Appendix 

## 2.1 Java EE Application Servers
Oracle REST Data Services supports Java EE application servers:

| Application Server | Supported Releases |
| --- | --- | 
|Oracle WebLogic Server | 14c or later | 
| Apache Tomcat | 8.5.x - 9.0.x | 

> Note: Tomcat Release 10 (in current docs says no, is that true?)

## 2.2 Oracle Application Express (APEX)

Oracle REST Data Services supports the currently supported versions of APEX. 

Can we just use this [link](https://www.oracle.com/us/assets/lifetime-support-technology-069183.pdf#%5B%7B%22num%22%3A154%2C%22gen%22%3A0%7D%2C%7B%22name%22%3A%22Fit%22%7D%5D)?

## 1.3 Prerequisites



### 1.3.2 

### 1.3.1 
## 1.3 Downloading ORDS



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

> [Return to the Guide](./1-ords-installation-checklist.md#12-user-requirements)