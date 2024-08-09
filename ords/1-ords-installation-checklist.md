# 1 Oracle REST Data Services Installation Checklist

This chapter provides information about supported platforms, system requirements, and Database privileges required for using ORDS.

## 1.1 System Requirements

Oracle REST Data Services system requirements are as follows:

- A supported Web Browser

  > Refer to Oracle Software Web Browser Support Policy for more information.

- A currently supported version of Oracle Database.

  > See Also: Oracle Lifetime Support Policy

Use \[of\] one of the following:

- Oracle Java version 11, 17, or 21
- Oracle GraalVM Enterprise Edition for Java version 11, 17, or 21

  > Note: ORDS installations will fail on Linux systems with an Oracle Java Version below JDK 11. Users will see the following error message:
  
  ```shell
  Error: ORDS requires Java 11 and above to run. Found Java version 1.
  Please set JAVA_HOME to appropriate version and update PATH if necessary.
  ```

  You must set your `JAVA_HOME` to the appropriate version and update the `PATH` if required.

  <details><summary style="color: dodgerblue;">What is <code>JAVA_HOME</code>?</summary><p></p>
  <code>JAVA_HOME</code> is one of many "Environment" variables used by your operating system. This particular variable indicates the location where the Java Development Kit (JDK) software is installed on your computer.<sup>1</sup><p></p>
  
  Within this location (the specific JDK directory, or folder) exist two more subdirectories:  

  - <code>bin/</code> - which contains the java executable, *and*
  - <code>lib/</code> - which contains the core java libraries and properties files<sup>2</sup><p></p>

  The <code>JAVA_HOME</code> Environment variable has many uses. And for Java programs, such as ORDS, to execute properly they depend on the <code>JAVA_HOME</code>> variable to identify where the JDK is located.  
  
  We'll revisit <code>JAVA_HOME</code>, but for now consider this brief illustration. Say you were dealing with JDK 11, then (depending on your operating system) you might find the JDK in these locations:

  - **Linux** `/usr/lib/jvm/jdk-11-oracle-x6` (or aarch64)<sup>3</sup>
  - **macOS** `/Library/Java/JavaVirtualMachines/jdk-11`<sup>4</sup>
  - **Windows** `/Program Files/Java/jdk-11`<sup>5</sup>
  </details>

  <details>
  <summary style="color: dodgerblue;">What is <code>PATH</code>?</summary><p></p>  
  
  > The *official* definition of `PATH`:
  >
  > This variable shall represent the sequence of path prefixes that certain functions and utilities apply in searching for an executable file. The prefixes shall be separated by a colon `:`. If the pathname being sought contains no slash `/` characters, and hence is a filename, the list shall be searched from beginning to end, applying the filename to each prefix and attempting to resolve the resulting pathname, until an executable file with appropriate execution permissions is found.  
  
  <code>PATH</code> is simply an environment variable that stores "shortcuts."  
  <p></p>
  &emsp;&emsp;<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-down-right" viewBox="0 0 16 16">
  <path fill-rule="evenodd" d="M14 13.5a.5.5 0 0 1-.5.5h-6a.5.5 0 0 1 0-1h4.793L2.146 2.854a.5.5 0 1 1 .708-.708L13 12.293V7.5a.5.5 0 0 1 1 0z"/></svg> efowfw f wfefff woefj
  &emsp;&emsp;nonadvnadnvnvnvnqlnvnvnvnvnvnvnnnnnvnvnvnnvnvn
  

  
  
  
  
  <sup>6</sup> https://www.geeksforgeeks.org/how-to-set-java-path-in-windows-and-linux/
  <p></p>
   
  
  </details>

  On Windows systems, you will be redirected to the Java download page to download the latest JDK.

<sup>1</sup>[JAVA_HOME](https://docs.oracle.com/javase/8/docs/technotes/guides/troubleshoot/envvars001.html#CIHEEHEI)  
<sup>2</sup>[NASA - Finding and Setting JAVA_HOME](https://pds.nasa.gov/datastandards/training/documents/Finding%20and%20Setting%20JAVA%20HOME.pdf)  
<sup>3</sup>[JDK Installation on Linux](https://docs.oracle.com/en/java/javase/11/install/installation-jdk-linux-platforms.html#GUID-737A84E4-2EFF-4D38-8E60-3E29D1B884B8)  
<sup>4</sup>[JDK Installation on macOS](https://docs.oracle.com/en/java/javase/11/install/installation-jdk-macos.html#GUID-2FE451B0-9572-4E38-A1A5-568B77B146DE)  
<sup>5</sup>[JDK Installation on Windows](https://docs.oracle.com/en/java/javase/11/install/installation-jdk-microsoft-windows-platforms.html#GUID-A7E27B90-A28D-4237-9383-A58B416071CA)  
<sup>6</sup>[How to Set Java Path in Windows and Linux?](https://www.geeksforgeeks.org/how-to-set-java-path-in-windows-and-linux/)