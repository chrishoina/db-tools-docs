# 1 Oracle REST Data Services Installation Checklist

This chapter provides information about supported platforms, system requirements, and Database privileges required for using ORDS.

## 1.1 System Requirements

Oracle REST Data Services system requirements are as follows:

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

> So, you must set JAVA_HOME to the appropriate version and update the PATH if required.
On Windows system, the user is re-directed to the Java download page.
• Web browser requirements: Refer to Oracle Software Web Browser Support Policy for more information.