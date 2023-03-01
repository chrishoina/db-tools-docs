# 1  Oracle REST Data Services Installation Checklist

## 1.1 System Requirements

|Component | Versions|
|      --- |    ---  | 
| Oracle Database<br>(*any of*) | 11g Release 2 or later<br>19c<br>21c | 
| Oracle Java | 11 *or* 17 |

## 1.2 Database Credendial Requirements

<!-- you need an account or use that script to create -->

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

## 1.4 Obtain the ORDS package

ORDS can be obtained via a zip file, or through the Yum repository.

### 1.4.1 Option 1: Zip file

The `ords_latest.zip` file can be downloaded from Oracle REST Data Services (ORDS) [download page](https://www.oracle.com/database/sqldeveloper/technologies/db-actions/download/). Once the zip file has been downloaded, unzip the `ords_latest.zip` folder.

> Note: The `ords_latest` folder contains the various subfolders and files required by ORDS; most importantly are the `bin`,`docs`, `examples`, `scripts`<sup>1</sup> folders.

<sup>1</sup>The `scripts` folder contains install privilege scripts, APEX migration scripts, as well as legacy ORDS scripts. They can be reviewed in detail in the Appendix.

Because the `ords_latest` folder contains application binary files, it is recommended that you relocate the entire `ords_latest` folder in a directory where other application binaries are located.

 <!-- into a folder of your choice. The folder you choose to unzip the file is referred to as the ORDS product folder. The ORDS product folder contains a bin folder and other folders and files required to run ORDS.  -->


### 1.4.2 Option 2: Yum


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

# 3 Installing and Configuring Oracle REST Data Services

> Oracle Linux, Windows, Mac, RPM

## 3.1 Single Instance or PDB
## 3.2 Multitenant Architecture
### 3.2.1 CDB
### 3.2.2 Application Container 
## 3.2 Customer Managed Autonomous Database
## 3.3 OCI Container
### 3.3.1 Docker
### 3.3.2 Podman 


# 4 Repairing Oracle REST Data Services
# 5 Upgrading Oracle REST Data Services
# 6 Uninstalling Oracle REST Data Services

