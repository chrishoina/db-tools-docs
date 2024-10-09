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

<details>
  <summary style="color: royalblue;">Should I use the Java JDK or GraalVM JDK?</summary><p></p>

  First of all, here is something you should know: Oracle GraalVM Enterprise Edition for Java has *several* releases across *several* versions of Java. For instance, consider Oracle GraalVM Enterprise Edition 21. Its referenced as 21 because of the year when it was first releases; a numbering convention observed through 2023.<sup>1</sup> But that 21 should *not* be confused with the version of Java it supports.  
  
  At the time of this writing there are archived releases, 19.3.1 - 22.3.5, of Oracle GraalVM Enterprise Edition. However, these archived versions, no longer in support, were and still are available for download for Java versions 8, 11, and 17. Although, I would not recommend using them since they are no longer being updated with security patches. Besides, any errors you experience in production would need to be reproduced with an ORDS-supported version of the Oracle JDK before a support request can even be filed!

  This leaves you with two options, Oracle GraalVM Enterprise Edition 20 Long-Term-Support Release for Java 8, and 11 *or* Oracle GraalVM Enterprise Edition 21 Long-Term-Support Release for Java 8, 11, or 17. Since Java 8 isn't supported by ORDS, then you are left with 11 or 17 
  GraalVM is a full-scale JDK distribution that can make Java applications run faster with a new advanced just-in-time compiler (Graal). As a platform it uses the Java HotSpot VM, so all tools and libraries that work on OpenJDK, work the same way on GraalVM JDK. In this context, GraalVM replaces the last-tier optimizing compiler in the JVM (C2) with the Graal compiler. This compiler is the outcome of 10+ years of research at Oracle Labs and includes several new optimizations, such as advanced inlining, partial escape analysis, code duplication, and speculative optimizations. GraalVM is itself written in Java, rather than C/C++, which simplifies maintenance and helps us develop and deliver new optimizations much faster.
</details>

  > Note: ORDS installations will fail on Linux systems with an Oracle Java Version below JDK 11. Users will see the following error message:
  
  ```shell
  Error: ORDS requires Java 11 and above to run. Found Java version 1.
  Please set JAVA_HOME to appropriate version and update PATH if necessary.
  ```

  You must set your `JAVA_HOME` to the appropriate version and update the `PATH` if required.

<details>
  <summary style="color: royalblue;">What is <code>JAVA_HOME</code>?</summary>
  <p>

  <code>JAVA_HOME</code> is one of many "Environment" variables used by your operating system. This particular variable indicates the location where the Java Development Kit (JDK) software is installed on your computer.<sup>2</sup>
  </p>

  Within this location (the specific JDK directory, or folder) exist two more subdirectories:  

- <code>bin/</code> - which contains the java executable, *and*
- <code>lib/</code> - which contains the core java libraries and properties files<sup>3</sup><p></p>

The <code>JAVA_HOME</code> Environment variable has many uses. And for Java programs, such as ORDS, to execute properly they depend on the <code>JAVA_HOME</code> variable to identify where the JDK is located.  
  
We'll revisit <code>JAVA_HOME</code>, but for now consider this brief illustration. Say you were dealing with JDK 11, then (depending on your operating system) you might find the JDK in these locations:

- **Linux** `/usr/lib/jvm/jdk-11-x64` (or aarch64 if not x64)<sup>4</sup>
- **macOS** `/Library/Java/JavaVirtualMachines/jdk-11`<sup>5</sup>
- **Windows** `/Program Files/Java/jdk-11`<sup>6</sup>

</details>

<details>
<summary style="color: royalblue;">What is <code>PATH</code>?</summary>
<p>  

The *official* definition of `PATH`:

>This variable shall represent the sequence of path prefixes that certain functions and utilities apply in searching for an executable file. The prefixes shall be separated by a colon `:`. If the pathname being sought contains no slash `/` characters, and hence is a filename, the list shall be searched from beginning to end, applying the filename to each prefix and attempting to resolve the resulting pathname, until an executable file with appropriate execution permissions is found.<sup>7</sup>  
</p>  

  <code>PATH</code> is simply an environment variable that stores "shortcuts" to executable files (maybe you've seen these referred to as `.exe` files).<sup>8</sup> Paths to executables can be listed too, separated by a colon <code>:</code> instead of say perhaps a comma <code>,</code>.  

  This reference to <code>PATH</code> is something that you'll see consistently whenever you download a new command line program. As an example, when you issue a command, like `ords serve` (as you'll see later) your command language interpreter (e.g., shell, zsh, bash, Command Prompt) will look to the `PATH` to see if an executable exists for that command you just entered. Subprograms (programs executed after or during an initial program execution) can do this too.

</details>

On Windows systems, you will be redirected to the Java download page to download the latest JDK.

<sup>1</sup> [Oracle GraalVM release calendar](https://docs.oracle.com/en/graalvm/release-calendar.html)  
<sup>2</sup> [JAVA_HOME](https://docs.oracle.com/javase/8/docs/technotes/guides/troubleshoot/envvars001.html#CIHEEHEI)  
<sup>3</sup> [NASA - Finding and Setting JAVA_HOME](https://pds.nasa.gov/datastandards/training/documents/Finding%20and%20Setting%20JAVA%20HOME.pdf)  
<sup>4</sup> [JDK Installation on Linux](https://docs.oracle.com/en/java/javase/11/install/installation-jdk-linux-platforms.html#GUID-737A84E4-2EFF-4D38-8E60-3E29D1B884B8)  
<sup>5</sup> [JDK Installation on macOS](https://docs.oracle.com/en/java/javase/11/install/installation-jdk-macos.html#GUID-2FE451B0-9572-4E38-A1A5-568B77B146DE)  
<sup>6</sup> [JDK Installation on Windows](https://docs.oracle.com/en/java/javase/11/install/installation-jdk-microsoft-windows-platforms.html#GUID-A7E27B90-A28D-4237-9383-A58B416071CA)  
<sup>7</sup> [Environment variables in POSIX.1-2024](https://pubs.opengroup.org/onlinepubs/9799919799/)  
<sup>8</sup> [How to Set Java Path in Windows and Linux?](https://www.geeksforgeeks.org/how-to-set-java-path-in-windows-and-linux/)