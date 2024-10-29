# Miscellaneous Configuration Options of Oracle REST Data Services

## 5.2.3 Using Jetty XML Configuration Files

This section describes how to configure Jetty server for additional functionality using Jetty XML configuration files.

> **NOTE:** Beginning with ORDS version 24.1, the standalone ORDS Access Log format was updated to include additional format codes.  
>
> |ORDS versions | Jetty Format codes used [^1] | Access Log example |  
> | --------------- | ------------------- | ------------------ |  
> | 23.4 and earlier | "%h %l %u %t "%r" %>s %b" | 127.0.0.1 - frank [10/Oct/2000:13:55:36 -0700] "GET /ords HTTP/1.1" 302 |  
> | 24.1 and later | "%{client}a %u %t "%r" %s %{CLF}O "%{Referer}i" "%{User-Agent}i" %{ms}T %{Host}i" | 192.168.122.1 - [27/Mar/2023:23:00:07 +0000] "GET /ords/ HTTP/1.1" 302 - "-" "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0" 132 192.168.122.149:8080 |  

[^1]: [About Jetty Custom Request Log format codes and syntax](https://javadoc.io/doc/org.eclipse.jetty/jetty-server/10.0.24/org.eclipse.jetty.server/org/eclipse/jetty/server/CustomRequestLog.html)

In most cases, the ORDS-provided Access Log data may be sufficient. However, should you choose to create your own custom Access Log, you may do so with Jetty XML files. [^2]

[^2]: Jetty XML files can be a simpler way for you to add additional configuration settings to your Jetty server without having to create a custom Jetty Module. For a deeper dive on Jetty modules and customization, [see here](https://jetty.org/docs/jetty/12/operations-guide/modules/index.html).
 

When ORDS is running in a standalone mode, the Eclipse Jetty Home is $ {configuration.directory}/global/standalone/. The Jetty XML syntax can be used to configure the Jetty Server for additional functionality by placing configuration XML files in the Jetty Home etc directory. The capability to do this is provided through the Eclipse Jetty server product.

### Examples

This section provides examples of augmenting Eclipse Jetty Server behaviour for additional functionalily. The following examples show how you can change Eclipse Jetty Server behaviour and not the ORDS behaviour. The location for Jetty XML files to be used by ORDS at the startup in standalone mode is: 

```sh
${configuration.directory}/global/standalone/etc/\
```

#### Example 5-2 Using a specific access log format

When the configuration setting standalone.access.log is provided, ORDS can produce an access log.
/global/standalone/etc/jetty-access-log.xml

```xml
<?xml version="1.0"?>
<!DOCTYPE Configure PUBLIC "-//Jetty//Configure//EN" "http://www.eclipse.org/ jetty/configure.dtd">
<Configure id="Server" class="org.eclipse.jetty.server.Server">
<Ref id="Handlers">
<Call name="addHandler">
<Arg>
<New id="RequestLog"
class="org.eclipse.jetty.server.handler.RequestLogHandler"> <Set name="requestLog">
<New id="RequestLogImpl" class="org.eclipse.jetty.server.CustomRequestLog">
<Arg>/ords/ords-access.log</Arg>
<Arg>%{remote}a - %u %t "%r" %s %O "%{Referer}i" "%{User-Agent}i"</Arg> </New>
</Set> </New>
</Arg> </Call>
</Ref> </Configure>
```

#### Example 5-3 Always returning a certain header in the response

Although this can also be achieved through a Load Balancer or Reverse Proxy in front of ORDS. If you want a specific header to be returned in every response from the ORDS server. Then use the following sample code snippet:
/global/standalone/etc/jetty-response.xml

```xml
<?xml version="1.0"?>
<!DOCTYPE Configure PUBLIC "-//Jetty//Configure//EN" "http://www.eclipse.org/ jetty/configure.dtd">
<Configure id="Server" class="org.eclipse.jetty.server.Server">
<Call name="insertHandler"> <Arg>
<New class="org.eclipse.jetty.rewrite.handler.RewriteHandler"> <Get id="Rewrite" name="ruleContainer" />
<Call name="addRule">
<Arg>
<New id="header"
class="org.eclipse.jetty.rewrite.handler.HeaderPatternRule"> <Set name="pattern">*</Set>
<Set name="name">Strict-Transport-Security</Set>
<Set name="value">max-age=31536000;includeSubDomains</Set> </New>
</Arg> </Call>
</New> </Arg>
Chapter 5
Configuring Jetty in ORDS Standalone Mode
 Example 5-2 Using a specific access log format
  5-8
</Call> </Configure>
```