# 2 Configuration and Installation of Oracle REST Data Services

## 2.1 Pre-installation configuration for a single instance database or Pluggable Database (PDB)

Prior to installing ORDS in a single instance database or Pluggable database you will need to complete the following steps:

- Download the ORDS product folder
- Configure the ORDS configuration directories

### 2.1.1 Downloading and configuring ORDS

You can download the specific version or you can download the latest. In this case, if you wanted latest.

There are two options for obtaining the latest version of ORDS. Either via a zip file, or through the Yum repository.

#### 2.1.1.1 Option 1: Zip file

##### Obtaining the ORDS Zip file

You may download the latest build from the Oracle REST Data Services [download page](https://www.oracle.com/database/sqldeveloper/technologies/db-actions/download/). Once the download has completed you will need to unzip the folder (`ords_<latest>.zip`) file into a folder of your choice. Through the course of these instructions, this folder will be referred to as the `<ords product folder>`.

<!-- Need to reorder this entire section BELOW THIS LINE -->
This `<ords product folder>` contains many folders, files, and automation scripts. In this section you will be focused on the `<bin>` folder, and later create (if one does not already exist) the <`configuration_ folder>`.

> Note: The `ords_latest` folder contains the various subfolders and files required by ORDS; most importantly are the `bin`,`docs`, `examples`, `scripts`<sup>1</sup> folders.

<sup>1</sup>The `scripts` folder contains install privilege scripts, APEX migration scripts, as well as legacy ORDS scripts. They can be reviewed in detail in the Appendix.

Because the `ords_latest` folder contains application binary files, it is recommended that you relocate the entire `ords_latest` folder in a directory where other application binaries are located.

<!-- Option could be the Home folder on MacOS - details here: https://support.apple.com/guide/mac-help/folders-that-come-with-your-mac-mchlp1143/mac -->

<!-- Need to reorder this entire section ABOVE THIS LINE -->

##### Configuring the `<bin>` folder

> Oracle recommends to add the ORDS bin folder to your operating system PATH
environment variable.

###### Configuring for the LINUX/UNIX

```sh
echo -e 'export PATH="$PATH:/<ords product folder>/bin"' >>
~/.bash_profile
```

> Note: You will need to restart your shell for this change to take effect.

###### Configuring for Windows

> Note: A command prompt with administrator privileges is required.

```cp
SetX PATH "%PATH%;<ords product folder>\bin"
```

> Note: You will need to restart your Command Prompt for this change to take effect.

###### Configuring for macOS

```bash
echo -e 'export PATH="$PATH:/<ords product folder>/bin"' >> ~/.zprofile
```

<!-- Open Finder.
Press Command-Shift-G to open the dialogue box.
Input the following search: /usr/local/bin -->

> Note: You will need to restart your Terminal for this change to take effect.

##### Setting up the Configuration Folder

This section describes how to set up the configuration folder structure.

New installation has the ORDS configuration files placed in the configuration folder. 

<!-- Is this automated? Need to check. -->
Configuration files from ORDS release 21.4.x or earlier are migrated to the configuration folder.

You can obtain the configuration folder location using one of the following options:

<!-- What is command option? -->
    Command option:

    Use the --config option to specify your configuration folder.

    Example:

    ords --config /path/to/conf install
    Environment variable:

    Note:This option is preferred if you forget to include the --config option when you are using the ORDS command-line Interface.
        ORDS_CONFIG: Create the ORDS_CONFIG environment variable.

        Example for LINUX or UNIX operating system:

Shell script containing ORDS_CONFIG
cat example_env
export ORDS_CONFIG=/path/to/conf

echo $ORDS_CONFIG
/path/to/conf

_JAVA_OPTIONS:

Example:

        export _JAVA_OPTIONS=-Dconfig.url=/Users/<username>/work/dbtools-dev/config
        ./ords-22.1.0.087.1756/bin/ords config list

        _JAVA_OPTIONS: -Dconfig.url=/Users/<username>/work/dbtools-dev/config

    Current Working Directory:

    If the --config <configuration_folder> option is not specified, and the ORDS_CONFIG environment variable is not defined, then your current working directory is used as the configuration folder.

    Example:

    If your current working directory is /path/to/conf, then it uses that location for your configuration folder.

Note:

    Oracle highly recommends you to ensure that ORDS does not create the configuration directory in the ORDS product folder. For example, you can have a configuration folder in the following location:

/Users/<user_name>/work/dbtools-dev/config/

<!-- Need to look where other similar 3rd party tools place their config folders; can we recommend placing there?   -->

The best practice is to have your configuration files separate from the application files, this makes maintenance and upgrades easier and more reliable.

The following command is no longer valid:

Example: java -jar ords.war install

If you specify the legacy commands using java -jar ords.war, you get the following warning message:

Warning: Support for executing: java -jar ords.war has been deprecated. Please add ords to your PATH and use the ords command instead. Run the following command to add ORDS to your PATH:

<!-- Is this a mistake?  -->

<Displays an example of adding the bin folder to your PATH>

Start a new terminal to pick up this change. Oracle recommends to add the ORDS product bin folder to your path.

#### 2.1.1.2 Option 2: Yum

- Yum repository
  - [OL7](https://yum.oracle.com/repo/OracleLinux/OL7/oracle/software/x86_64/)
  - [OL8](https://yum.oracle.com/repo/OracleLinux/OL8/oracle/software/x86_64/)

<!-- I have confirmed that ORDS is available in OL9 -->
  - [OL9](https://yum.oracle.com/repo/OracleLinux/OL9/oracle/software/x86_64/)  

<!-- It gets muddled when dealing with Yum and RPM. I'll need to run through an install and config of each to better understand which directions go where.  -->

### 2.1.2 Multi-Tenant Container Database (CDB)

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

Uninstall and install in same chapter
Maybe have (depending on template) upgrade, repair, and uninstall (this depends on the length as well).

