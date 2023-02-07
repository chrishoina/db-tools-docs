# 1  Oracle REST Data Services Installation Checklist

## 1.1 System Requirements

|Component | Versions|
|      --- |    f---  | 
| Oracle Database<br>(*any of*) | 11g Release 2 or later<br>19c<br>21c
| Oracle Java | 11 *or* 17 |

## 1.2 User Requirements

- As SYSDBA, or
- Using the included ORDS Installer Privileges Script<sup>1</sup>; grant privileges<sup>2</sup> allowing a user to, in either an Oracle Pluggable Database (PDB) or Oracle 11g, perform the following ORDS actions:
  - installation
  - repair
  - uninstallation

<sup>1</sup>About [the script](./appendix.md#aboutthescript)

<sup>2</sup>Review [the privileges](./appendix.md#reviewprivileges)

## 1.3 Command Line Tool

ORDS 22.1.0 and later requires a command line tool for installation. Options include:

| Recommended<br>Command Line Interface |
|                   ---                 |
|           SQLcl<sup>1</sup>           |

<sup>1</sup>About SQLcl: [Overview and help](./appendix.md#1.3abouttheordscommandlinetool).

# 2 Currently supported Applications and Application Servers

## 2.1 Java EE Application Servers
Oracle REST Data Services supports Java EE application servers:

| Application Server | Supported Releases |
| --- | --- | 
|Oracle WebLogic Server | 14c or later | 
| Apache Tomcat<sup>1</sup> | 8.5.x - 9.0.x | 

## 2.2 Oracle Application Express (APEX)

Oracle REST Data Services supports all APEX versions in Premier Support status<sup>1</sup>.

<sup>1</sup>[APEX versions](https://www.oracle.com/us/assets/lifetime-support-technology-069183.pdf#%5B%7B%22num%22%3A154%2C%22gen%22%3A0%7D%2C%7B%22name%22%3A%22Fit%22%7D%5D) in Premier Support.

