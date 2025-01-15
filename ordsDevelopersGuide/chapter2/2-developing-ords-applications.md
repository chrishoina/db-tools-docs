<!-- https://oracle-my.sharepoint.com/personal/tulika_das_oracle_com/_layouts/15/onedrive.aspx?csf=1&web=1&e=7EGLVb&CID=a41001e8%2D3a7e%2D403f%2D9234%2D713d44bb73d6&id=%2Fpersonal%2Ftulika%5Fdas%5Foracle%5Fcom%2FDocuments%2FTD%20Projects%2FORDS%20Doc%20Revamp%202023&FolderCTID=0x0120004335BE87777DC644A1BD73BDB63CA75D&view=0

Example pandoc 3-implicit-parameters.md -f markdown -t docx -o 3-implicit-parameters.md.docx -->

# 2 Developing Oracle REST Data Services Applications

## 2.9 JWT Bearer Token Authentication and Authorization Using the ORDS JWT Profile

ORDS release 23.3 introduced support for JSON Web Tokens (JWTs) beginning with version 23.3.

JWTs enable developers to delegate authentication and subsequent authorization of users, clients and applications to access protected ORDS endpoints (i.e. Resources, APIs). ORDS supports JWT authentication/authorization with any OAuth2-compliant Identity Provider, such as: OCI Identity Access Management, Microsoft Entra (formerly known as Microsoft Azure Active Directory), Okta, Auth0, among others.

### How it works

ORDS acts as a resource server in a typical OAuth 2.0 [^2.9] (or OpenID Connect) flow, making it convenient for clients, users, developers, applications to access protected ORDS APIs from with a web application.

You can create a JWT Profile for any REST-Enabled schema to provide ORDS with a
mechanism to validate JWT bearer tokens. If a JWT bearer token is validated, then ORDS
accepts the following:
• The JWT subject claim as the authenticated user making the request
• The JWT scope claims as the REST-Enabled schemas ORDS privileges that the user has
consented to the application using the privileges on their behalf

Topics:
• About JSON Web Tokens (JWTs)
• Prerequisites for JWT Authentication
• Creating an ORDS JWT Profile
• JWT Identity Provider Details
• Making Requests to ORDS Using a JWT Bearer Token
• About JSON Web Tokens (JWTs)
This section introduces you to the JSON Web Tokens.
• Prerequisites for JWT Authentication
This section lists the prerequisites for JWT authentication.
• Creating an ORDS JWT Profile
This section explains how to create an ORDS JWT Profile.
• JWT Identity Provider Details
• Making Requests to ORDS Using a JWT Bearer Token

[^2.9] https://datatracker.ietf.org/doc/html/rfc6749#section-1.2

### 2.9.1 About JSON Web Tokens (JWTs)
This section introduces you to the JSON Web Tokens.
A JSON Web Token (JWT) is a compact, URL-safe means of representing claims to be
transferred between two parties. The claims in a JWT are encoded as a JSON object. ORDS
supports the use of any OAuth2-compliant identity providers such as, OCI IAM with Identity
Domains, Oracle Identity Cloud Service (IDCS), Auth0, and Okta. If a JWT is required to
access a resource, ORDS validates the JWT using a corresponding public verification key
provided by the authorization server.
A JWT comprises of the following:
• A header, that identifies the type of token and the cryptographic algorithm used to generate
the signature.

The header is required to contain the following reserved claims.
Note:
A claim is a key value pair, where the key is the name of the claim.
* alg (algorithm)
* kid (key id)
– The header can optionally contain the following reserved claims that ORDS takes into
account
* x5t (x.509 certificate thumbprint)
* typ (type)
– The header can also contain custom claims with user-defined names.

A payload containing claims about the identity of the end user, and the properties of the
JWT.
– A payload is required to contain the following reserved names of the claims:
* sub (subject)
* aud (audience)
* iss (issuer)
* iat (issued at)
* exp (expiration time)
– The payload can optionally contain the following reserved claims that ORDS takes into
account
* scope or scp
* nbf (not before)
– A payload can also contain custom claims with user-defined names
• A signature, to validate the authenticity of the JWT (derived by base64 encoding the
header and the payload).
When using JWTs to control access to the target schema APIs or resources, the JWT
Profile in the REST-Enabled schema specifies that the reserved claims in the payload of
the JWT must have particular values before ORDS considers the JWT to be valid.
ORDS only accepts the following:
– alg (algorithm) values of RS256, RS384 and RS512
– kid (key id) value that can be matched to a corresponding public verification key
– x5t (x.509 certificate thumbprint) if present to a corresponding public verification key
– typ (type) if present, requires the value to be JWT
– aud (audience) that matches the target schemas JWT Profile audience
– iss (issuer) that matches the target schema JWT Profile issuer
iat (issued at ) identifies the time when the JWT was issued and is not be accepted
before this time. This claim is used to determine the age of the JWT and enforce the
JWT Profile allowed age if it is set.
– exp (expiration time) identifies the expiration time when or after which the JWT is not
accepted for processing.
– nbf (not before) if present, identifies the time before which the JWT is not accepted for
processing.
When a JWT is validated and the payload of JWT contains the scope claim, the ORDS
privilege name protecting the resource is verified as being provided in the scope claim before
processing.

### 2.9.2 Prerequisites for JWT Authentication
This section lists the prerequisites for JWT authentication.
Before ORDS can accept authentication and authorization using JWTs:
• An OAuth2-compliant identity provider (for example, OCI IAM with Identity Domains,
Oracle Identity Cloud Service (IDCS), Auth0) must have already been set up to issue JWTs
for users who are allowed to access the ORDS resources.
• If you want to use custom claims in authorization policies, the identity provider must be set
up to add the custom claims to the JWTs that it issues.
See Also:
• Managing Applications
• Oracle Identity Cloud Service
• Auth0, an identity platform to manage access to your applications.
To validate a JWT using a corresponding public verification key provided by the issuing identity
provider:
• the signing algorithm used to generate the signature of JWT must be one of RS256, RS384,
or RS512
• the public verification key must have a minimum length of 2048 bits and must not exceed
4096 bits
• the public verification key must be specified using the JSON Web Key (JWK) format and
ORDS can access it without authentication
The JWK URI
• The URI must be routable from the subnet containing ORDS
• Certain key parameters must be present in the JWKS to verify the signature of the JWT.
See Parameters for Verifying JWT Signatures.
• By default, the JWKS can be up to 10000 bytes in size

### 2.9.3 Creating an ORDS JWT Profile
This section explains how to create an ORDS JWT Profile.
A JWT Profile can be created within a REST-Enabled schema using the
OAUTH.CREATE_JWT_PROFILE procedure. Alternatively, OAUTH_ADMIN.CREATE_JWT_PROFILE can
be used to create a JWT Profile in other REST-Enabled schemas as long as the user has the
ORDS_ADMINISTRATOR role.
Note:
Only one JWT Profile can be defined per schema. To update an existing JWT Profile,
the existing JWT Profile must be deleted before creating a new one.
Example:
BEGIN
OAUTH.CREATE_JWT_PROFILE(
p_issuer => 'https://identity.oraclecloud.com/',
p_audience => 'ords/myapplication/api' ,
p_jwk_url =>'https://
idcs-10a10a10a10a10a10a10a10a.identity.oraclecloud.com/admin/v1/SigningCert/
jwk'
);
COMMIT;
END;
/
This JWT Profile specifies the issuer, audience, and the JWK URL.
Additionally, an allowed skew and age can be specified. The p_issuer must be a non null
value and must match the iss claim in the JWT bearer token. The p_audience must be a non
null value and must match with the aud claim in the JWT bearer token.
The p_jwk_url must be a non null value starting with https:// and identify the public
verification key provided by the authorization server in a JSON Web Key (JWK) format.
Once the JWT Profile has been created, requests made to the schema protected resources
can be accessed by providing a valid JWT bearer token with the scope to access the protected
resource.

Note:
A JWT scope claim is a JSON string containing a space-separated list of scopes. A
protected ORDS resource is protected with a named ORDS privilege. To access the
protected ORDS resource, the JWT scope claim must contain a scope with the same
name as the protecting ORDS privilege. The scope of an ORDS privilege are case
sensitive.
See Also:
OAUTH PL/SQL Package Reference

### 2.9.4 JWT Identity Provider Details
The identity provider that issued the JWT, determines the values that are allowed to specify for
the issuer (iss), and the audience (aud) claims in the JWT. The identity provider that issued the
JWT also determines the URI from where to retrieve the JSON Web Key Set (JWKS) to verify
the signature of the JWT.

Identity Provider Issuer (iss) claim Audience (aud) Claim Format of URI from
which to Retrieve the
JWKS
Okta https://<your-okta-
tenant-name>.com
Customer-specific.
The audience configured
for the Authorization
Server in the Okta
Developer Console.
https://<your-okta-
tenant-name>.com/
oauth2/<auth-
server-id> /v1/keys
IDCS https://
identity.oracleclou
d.com/
Customer-specific.
Refer to "Validating
Access Tokens" section
in Oracle Identity Cloud
Service documentation.
https://<tenant-
base-url>/admin/v1/
SigningCert/jwk
To obtain the JWKS
without logging in to
Oracle Identity Cloud
Service, refer to
"Change Default
Settings" in Oracle
Identity Cloud Service
documentation.
OCI IAM with Identity
Domains
https://
identity.oracleclou
d.com
Customer-specific.
See "Managing
Applications" section in
OCI IAM with Identity
Domains documentation.
https://<tenant-
base-url>/admin/v1/
SigningCert/jwk
Auth0 https://<your-
account-
name>.auth0.com/
Customer-specific. https://<your-
account-
name>.auth0.com/.we
ll-known/jwks.json

Parameters for Verifying JWT Signatures
This section lists the key parameters required to verify the JWT signatures.
• JWT Scopes and ORDS Privileges
• JWT Subject

See Also:
• Validating Access Tokens in Oracle Identity Cloud Service documentation.
• Change Default Settings in Oracle Identity Cloud Service documentation.
• Managing Applications in OCI IAM with Identity Domains documentation.

#### 2.9.4.1 Parameters for Verifying JWT Signatures
This section lists the key parameters required to verify the JWT signatures.
To verify the signature on a JWT, ORDS requires that the key parameters are present in the
JWKS returned from an URI.
Key Parameter Notes
kid The identifier of the key used to sign the JWT. The
value must match the kid claim in the JWT header.
For example, master_key.
kty The type of the key used to sign the JWT. Note that
RSA is currently the only supported key type.
n The public key modulus.
e The public key exponent.
alg The signing algorithm (if present) must be set to
one of RS256, RS384 or RS512.

#### 2.9.4.2 JWT Scopes and ORDS Privileges
You must configure the identity provider that issued the JWT, so as to provide the scope that
matches the desired ORDS privilege. If a resource is protected in ORDS using an ORDS
privilege, then that privilege name must be defined as a scope. The scope is then available for
the application to request on behalf of the user. The issued JWT must then provide that as a
scope claim.
Typically, identity providers allow APIs, resources, or scopes to be defined for a particular
audience. For example: ORDS REST-Enabled schema defined API. These APIs, resources, or
scopes can then be made available to specific applications or clients. The application can then
request access tokens on behalf of an authenticated user for that audience and scope.
More than one scope can be requested and provided in the JWT. The protected ORDS
resource is accessible as long as one of the scopes matches the ORDS privilege protecting
the resource.

#### 2.9.4.3 JWT Subject
ORDS accepts the subject (sub) claim in a valid JWT bearer token as the unique identifier for
the user who consented for the application to access their data.
The value of the subject claim in a valid JWT bearer token is bound to the :current_user implicit
parameter and the REMOTE_IDENT OWA CGI environment variable.

### 2.9.5 Making Requests to ORDS Using a JWT Bearer Token
Once a JWT Profile has been created for a REST-Enabled schema, the protected ORDS
resources in that schema can be accessed by providing a valid JWT bearer token with the
request.
Request to an ORDS protected resource is made from a third party application on behalf of a
user. The third party application has configured its authentication using an Identity Provider.
The same Identity Provider can be configured to issue JWT access tokens for ORDS. After the
third party application has acquired a JWT access token from the Identity Provider, it can

include the JWT as a bearer token in requests to ORDS. Third party application can request
suitable JWT access tokens with the required scope to access the ORDS resource.

curl -X GET http://localhost:8080/ords/myapplication/api/sales / --header "Authorization: Bearer
$JWT"

## 2.16 Overview of Pre-hook Functions

This section explains how to use PL/SQL-based pre-hook functions with ORDS. An ORDS pre-hook function is a `BOOLEAN` function that returns a `TRUE` or `FALSE`. Once an ORDS pre-hook function has been defined and configured, the pre-hook function will be invoked prior to satisfying an ORDS `REST` request. The examples contained in this section illustrate several scenarios of how and when an ORDS pre-hook function can be used.

ORDS pre-hook functions are typically used to implement application logic that needs to be applied across all REST endpoints of an application. Pre-hook functions can be used for, but not limited to, scenarios such as:

- Configuring database session-based application context to support a Virtual Private Database (VPD) policy.[^1]
- Customizing authentication and authorization.[^2]
- Enabling auditing or metrics gathering.

[^1]: I'd consider this a rather advanced use case. In this scenario, you would create a PL/SQL package to set an application context (along with a trigger), followed by a function that would permit users to view certain resources (APIs). There is a "simple" tutorial, [here](https://docs.oracle.com/en/database/oracle/oracle-database/19/dbseg/using-oracle-vpd-to-control-data-access.html#GUID-2113CF3C-D950-40B3-A121-A44284EF104D) that details the steps for creating a Virtual Private Database (VPD) policy. However, you do not need to complete the tutorial to understand how something like this would work in practice. If you compare the steps in that tutorial to what is included in the `custom_auth_api.plb` and `custom_auth_api.pls` package body and spec of this ORDS tutorial, you'll notice some parallels. Essentially, you can create some rather novel functions, procedures, and triggers; ones that will be invoked via that ORDS pre-hook `BOOLEAN` (i.e.,  `TRUE / FALSE` ) function. But in the end, *everything* boils down to whether the pre-hook function (and any underlying subprograms) returns either a `TRUE` or `FALSE`. Learn more about "contexts" by reviewing the `SYS_CONTEXT`function in the [SQL Language Reference guide](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/SYS_CONTEXT.html).

[^2]: In this example, a pre-hook function can be invoked prior to satisfying an ORDS request. Such a pre-hook could (1) inspect the request headers (much like you'll see in this section's `.plb` and `.pls` file contents) (2) identify the user who is making the request, and  (3) determine if that user is authorized to make the request. In fact, you have a lot of options for which environment variables you might want to choose from.  

<details>
  <summary><b>Example:</b> Creating an ORDS <code>GET</code> request to retrieve CGI Environment variables from the <code>PRINT_CGI_ENV</code> PL/SQL utility.</summary>
  <p>

For instance, here is a quick way for you to learn some more about ORDS Resource Modules *and* about **C**ommon **G**ateway **I**nterface (CGI) Environment variables as they relate to the Oracle database. We'll rely upon the `OWA_UTIL` PL/SQL package, specifically the [`PRINT_CGI_ENV` procedure](https://docs.oracle.com/en/database/oracle/oracle-database/19/arpls/OWA_UTIL.html#GUID-F9AA35ED-76A8-428B-A7A6-3AEE698B8CE7) (an `HTML utility`; one of three [utility subprograms](https://docs.oracle.com/en/database/oracle/oracle-database/19/arpls/OWA_UTIL.html#GUID-7915F61E-1E50-4507-87FC-7E0ECAE3D41D) in the `OWA_UTIL` package). First, create a Resource Module and Template. Then, when creating a Handler, choose `plsql/block` as the `Source Type` and use the `PRINT_CGI_ENV` procedure in the Handler code. Like this:  

```sql
Begin 
  OWA_UTIL.PRINT_CGI_ENV;
End;
```  

![Handler code with PRINT_CGI_ENV procedure.](./images/handler-code-print-cgi-variables.png " ")*Sample Handler code*
![Exporting PL/SQL definitions.](./images/export-print-cgi-plsql-module.png " ")*Rmember you can export your Modules in PL/SQL.*
![A review of the Resource Module used in this example.](./images/plsql-slider-displaying-plsql-module.png " ")*Export Module SQL slider.*

Save your code and Handler.

**Sample code**

```sql
  BEGIN
  ORDS.ENABLE_SCHEMA(
      p_enabled             => TRUE,
      p_schema              => 'ORDSDEMO',
      p_url_mapping_type    => 'BASE_PATH',
      p_url_mapping_pattern => 'ordsdemo',
      p_auto_rest_auth      => FALSE);

  ORDS.DEFINE_MODULE(
      p_module_name    => 'scratch.pad',
      p_base_path      => '/v1/',
      p_items_per_page => 25,
      p_status         => 'PUBLISHED',
      p_comments       => NULL);

  ORDS.DEFINE_TEMPLATE(
      p_module_name    => 'scratch.pad',
      p_pattern        => 'oga-cgi-example',
      p_priority       => 0,
      p_etag_type      => 'HASH',
      p_etag_query     => NULL,
      p_comments       => NULL);

  ORDS.DEFINE_HANDLER(
      p_module_name    => 'scratch.pad',
      p_pattern        => 'oga-cgi-example',
      p_method         => 'GET',
      p_source_type    => 'plsql/block',
      p_mimes_allowed  => NULL,
      p_comments       => NULL,
      p_source         => 
'begin
    OWA_UTIL.PRINT_CGI_ENV;
end;');

COMMIT;

END;
```

From there, either copy and paste this Handler's URI into a new terminal session (if using a tool like a curl), Postman (or a similar testing tool), or simply navigate to the URI in a new browser tab or window. What you'll see are all the CGI Environment variables that are sent back (in an *unauthenticated* server response) to you, a client, or an application. Pretty neat trick, eh?  

Here is an example of the response from an Autonomous Database - Always Free tenancy:  

![Reviewing CGI variables in an ADB Always Free tenancy.](./images/displaying-cgi-environment-variables-in-adb-no-query-string.png " ")  

Here is a curl command response from a development configuration (i.e., A locally installed ORDS instance running in Standalone mode and a 23ai database in a Podman container). [Learn more about ORDS and Podman](https://followthecoffee.com/category/podman/):  

![Reviewing CGI variables with ORDS standalone, on localhost.](./images/curl-command-in-podman%20container-cgi-variables.png " ")  

As you can see, there is a ton of data to work with. This is something to keep in mind if you want to use CGI Environment variables with your ORDS pre-hook (YOU DO NOT HAVE TO, this is just an example!).  

You might want to start small by implementing a security policy using something as simple as the `QUERY_STRING` variable (e.g., your ORDS pre-hook calls upon an underlying function or procedure that uses a Query string as a parameter.)  

Look what happens when I append `?chris` to the end of this URI:  

![Adding a query string to the end of the URI.](./images/adding-query-parameter-to-cgi-endpoint.png " ")  

If you take a close look, you can see how simple and automatic this is. Something to think about. Even if you don't care about CGI Environment variables *today*, I guarantee this will come in handy in the future.  

![New GCI environment variables with query string.](./images/displaying-print-out-adb-with-query-string.png " ")

[Return to top](#216-overview-of-pre-hook-functions)

</p>

</details>

### 2.16.1 Configuring the Pre-hook Function

~~This section describes how to configure a pre-hook function.~~  
Once you have performed the required steps in the database, you'll configure ORDS so that it is "aware" and expecting this *stored* pre-hook function. You can configure the pre-hook function in ORDS with the ORDS CLI command:

```shell
ords config set procedure.rest.preHook [schema where pre-hook function is defined.pre-hook function name]
```

![Using the ORDS CLI to set the pre-hook configuration setting.](./images/error-response-confirmation-auto.png " ")

You'll receive confirmation of the new setting in your terminal, but you can also review the settings using the `ords config list --include-defaults` command, as well as reviewing the pool.xml configuration file for the related database pool.

![ORDS configuration settings, reviewing the procedure.rest.preHook setting.](./images/reviewing-ords-config-settings-in-terminal.png " ")

![ORDS configuration, reviewing the pool xml file.](./images/reviewing-ords-configuration-in-settings-xml.png " ")

<!-- Need to include: 
Note about fully-qualified name: BEST PRACTICE https://oracle-one.slack.com/archives/C6V4QHPQA/p1730135103935539?thread_ts=1729799529.640709&cid=C6V4QHPQA -->

### 2.16.2 Using a Pre-hook Function

~~This section explains how the pre-hook function is used.~~
An ORDS pre-hook PL/SQL function must:

1. have zero arguments
2. return a BOOLEAN value
3. be executable by the database user (the user who is issuing the initial HTTP request) or executable by `PUBLIC`[^7]

[^7]: The original documentation reads as follows: *"A pre-hook must be a PL/SQL function with no arguments and must return a `BOOLEAN` value. <mark>The function must be executable by the database user to whom the request is mapped.</mark> For example, if the request is mapped to an ORDS enabled schema, then that schema must be granted the execute privilege on the pre-hook function (or to PUBLIC)."* The highlighted text might be confusing for some. All this means is that if say, `ORDS_TEST` user issues a `GET` request to `localhost:8080/ords/api` and *there is* an ORDS pre-hook function configured, the `ORDS_TEST` user needs to be able to `EXECUTE` that ORDS pre-hook function. Later in the docs you will explore the examples. and contained in those examples you will notice that the ORDS pre-hook functions have been `GRANT`ed `EXECUTE TO PUBLIC`; meaning *all users* can execute the ORDS pre-hook. [About the `GRANT` statement](https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/GRANT.html).

> **NOTE:** If using Oracle APEX 24.1 or higher, the `APEX_PUBLIC_ROUTER` user must be granted the `EXECUTE` privilege to ensure friendly URLs (i.e., `/r`) remain accessible. About [APEX Friendly URLs](https://docs.oracle.com/en/database/oracle/apex/24.1/htmdb/understanding-friendly-url-syntax.html#GUID-716B85EC-2D9B-49F7-BABE-2C4CA347F198).

#### ORDS Pre-hook function returns `TRUE`

When the ORDS pre-hook function returns `TRUE`, then normal processing will continue (e.g., an initial HTTP request will proceed).

ORDS invokes a pre-hook function in an OWA (Oracle Web Agent) that is a PL/SQL Gateway Toolkit environment. This means that the function can introspect the request headers and the OWA CGI environment variables, and use that information to drive its logic. The function can also use the OWA PL/SQL APIs to generate a response for the request (for example, in a case where the pre-hook function needs to abort further processing of the request, and provide its own response).

#### ORDS Pre-hook function returns `FALSE`

true, then it indicates that the normal processing of the request must continue. If the function returns false, then it indicates that further processing of the request must be aborted.

### 2.16.3 Processing of a Request

The pre-hook function must return true if it determines that the processing of a request must continue. In such cases, any OWA response produced by the pre-hook function is ignored (except for cases as detailed in the section Identity Assertion of a User), and the REST service is invoked as usual.

### 2.16.4 Identity Assertion of a User

This section describes how pre-hook function can make assertions about the identity of the user.
When continuing processing, a pre-hook can make assertions about the identity and the roles assigned to the user who is making the request. This information is used in the processing of the REST service. A pre-hook function can determine this by setting one or both of the following OWA response headers.
• X-ORDS-HOOK-USER: Identifies the user making the request, the value is bound to
the :current_user implicit parameter and the REMOTE_IDENT OWA CGI environment variable.
• X-ORDS-HOOK-ROLES: Identifies the roles assigned to the user. This information is used to determine the authorization of the user to access the REST service. If this header is present then X-ORDS-HOOK-USER must also be present.

Note:
X-ORDS-HOOK-USER and X-ORDS-HOOK-ROLES headers are not included in the response of the REST service. These headers are only used internally by ORDS to propagate the user identity and roles.
Using these response headers, a pre-hook can integrate with the role based access control model of ORDS. This enables the application developer to build rich integrations with third party authentication and access control systems.

### 2.16.5 Aborting Processing of a Request

This section explains how the pre-hook function aborts the processing of a request.
If a pre-hook determines that the processing of the REST service should not continue, then the function must return false value. This value indicates to ORDS that further processing of the request must not be attempted.
If the pre-hook does not produce any OWA output, then ORDS generates a 403 Forbidden error response page. If the pre-hook produces any OWA response, then ORDS returns the OWA output as the response. This enables the pre-hook function to customize the response that client receives when processing of the REST service is aborted.

### 2.16.6 Ensuring Pre-hook is Executable

If a schema cannot invoke a pre-hook function, then ORDS generates a 503 Service Unavailable response for any request against that schema. Since a pre-hook has been configured, it would not be safe for ORDS to continue processing the request without invoking the pre-hook function. It is very important that the pre-hook function is executable by all ORDS enabled schemas. If the pre-hook function is not executable, then the REST services defined in those schemas will not be available.

### 2.16.7 Exceptions Handling by Pre-hook Function

When a pre-hook raises an error condition, for example, when a run-time error occurs, a NO DATA FOUND exception is raised. In such cases, ORDS cannot proceed with processing of the REST service as it would not be secure. ORDS inteprets any exception raised by the pre-hook function as a signal that the request is forbidden and generates a 403 Forbidden response, and does not proceed with invoking the REST service. Therefore, if the pre-hook raises an unexpected exception, it forbids access to that REST service. It is highly recommended that all pre-hook functions must have a robust exception handling block so that any unexpected error conditions are handled appropriately and do not make REST Services unavailable.

### 2.16.8 Pre-hook Function Efficiency

A pre-hook function is invoked for every REST service call. Therefore, the pre-hook function must be designed to be efficient. If a pre-hook function is inefficient, then it has a negative effect on the performance of the REST service call. Invoking the pre-hook involves at least one additional database round trip. It is critical that the ORDS instance and the database are located close together so that the round-trip latency overhead is minimized.

### 2.16.9 Using Pre-hook Function with Protected Resources

ORDS enables the protection of resources with roles and privileges. In cases where:
• A privilege protects a particular resource
• A pre-hook function already exists
ORDS invokes pre-hook functions once the initial request to the target resource has been authorized. If an incoming request fails authorization, ORDS does not invoke a related pre- hook function. Instead, ORDS responds with a 401 Unauthorized Response status code.

See Also:
Configuring Secure Access to RESTful Services

### 2.16.10 Pre-Hook Examples

This section provides some sample PL/SQL functions that demonstrate different ways in which the pre-hook functionality can be leveraged.
Source code for the examples provided in the following sections is included in the unzipped Oracle REST Data Services distribution archive examples/pre_hook/sql sub-folder.

#### 2.16.10.1 Installing the Examples

This section describes how to install the pre-hook examples.

To install the pre-hook examples, execute examples/pre_hook/sql/install.sql script. The following code snippet shows how to install the examples using Oracle SQLcl command line interface:
pre_hook $ cd examples/pre_hook/sql/ sql $ sql system/<password>
SQLcl: Release Release 18.1.1 Production on Fri Mar 23 14:03:18 2018 Copyright (c) 1982, 2018, Oracle. All rights reserved.
Password? (**********?) ******
Connected to:
Oracle Database 12c Enterprise Edition Release 12.2.0.1.0 - 64bit Production
SQL> @install <chosen-password>
• You need to adjust the SQLcl connect string and the user credentials to suit your environment. For these demo scenarios, SQLcl connects to the database with service name orcl.
• <chosen-password> is the password you assigned to the PRE_HOOK_TEST database user. Make a note of this password value for later reference.
• The examples/pre_hook/sql/install.sql command creates the following two databases schemas:
– The PRE_HOOK_DEFNS schema where the pre-hook function is defined along with a database table named custom_auth_users, where user identities are stored. This table is populated with a single user joe.bloggs@example.com, whose password is the value assigned for <chosen-password>.
– The PRE_HOOK_TESTS schema where ORDS based REST services that are used to demonstrate the pre-hooks are defined.

##### 2.16.10.1.1 Example: Denying all Access

The simplest pre-hook is one that unilaterally denies access to any REST Service.
To deny access to any REST service, the function must always return false as shown in the following code snippet:

```sql
create or replace function deny_all_hook return boolean as begin
return false;
end;
/
grant execute on deny_all_hook to public;
```

Where:

• The deny_all_hook pre-hook function always returns false value.
• Execute privilege is granted to all users. So, any ORDS enabled schema can invoke this
function
Configuring ORDS
To enable deny_all_hook pre-hook function, perform the following steps:
1. Locate the folder where the Oracle REST Data Services configuration file is stored.
2. Open the settings.xml file and add:
<entry key="procedure.rest.preHook">pre_hook_defns.deny_all_hook</entry>
3. Save the file.
4. Restart Oracle REST Data Services.
Try it out
The install script creates an ORDS enabled schema and a REST service which can be accessed at the following URL (assuming ORDS is deployed on localhost and listening on port 8080) :
http://localhost:8080/ords/pre_hook_tests/prehooks/user
Access the URL in a browser. You should get a response similar to the following:
403 Forbidden
This demonstrates that the deny_all_hook pre-hook function was invoked and it prevented the
access to the REST service by returning a false value.

##### 2.16.10.1.2 Example: Allowing All Access

Modify the source code of the deny_all_hook pre-hook function to allow access to all REST service requests as shown in the following code snippet:
create or replace function deny_all_hook return boolean as begin
return true; end;
/
Try it out
Access the following test URL in a browser:
http://localhost:8080/ords/pre_hook_tests/prehooks/user

The response should include JSON similar to the following code snippet:
{
"authenticated_user": "no user authenticated"
}

Note:
The REST service executes because the pre-hook function authorized it.

Related Topics
• Identity Assertion of a User
This section describes how pre-hook function can make assertions about the identity of the user.

##### 2.16.10.1.3 Example: Asserting User Identity

The following code snippet demonstrates how the pre-hook function makes assertions about the user identity and the roles they possess:
create or replace function identity_hook return boolean as begin
if custom_auth_api.authenticate_owa then custom_auth_api.assert_identity; return true;
end if;
custom_auth_api.prompt_for_basic_credentials('Test Custom Realm'); return false;
end;
The pre-hook delegates the task of authenticating the user to the custom_auth_api.authenticate_owa function. If the function indicates that the user is authenticated, then it invokes the custom_auth_api.assert_identity procedure to propagate the user identity and roles to ORDS.
Configuring ORDS
To enable pre-hook function, perform the following steps:
1. Locate the folder where the Oracle REST Data Services configuration file is stored.
2. Open the settings.xml file and add:
<entry key="procedure.rest.preHook">pre_hook_defns.identity_hook</entry></ entry>
3. Save the file.
4. Restart Oracle REST Data Services.
Try it out
The install script creates an ORDS enabled schema and a REST service that can be accessed at the following URL (assuming ORDS is deployed on localhost and listening on port 8080):

http://localhost:8080/ords/pre_hook_tests/prehooks/user
In a web browser access the preceding URL.

Note:
The first time you access the URL, the browser will prompt you to enter your credentials. Enter the user name as joe.bloggs@example.com and for the password, use the value you assigned for <chosen-password> when you executed the install script. Click the link to sign in.

In response a JSON document is displayed with the JSON object in it.
{"authenticated_user":"joe.bloggs@example.com"}

#### 2.16.10.2 Uninstalling the Examples

This section explains how to uninstall the examples.
The following code snippet shows how to uninstall the examples:
pre_hook $ cd sql/
sql $ sql system/<password>
SQLcl: Release Release 18.1.1 Production on Fri Mar 23 14:03:18 2018 Copyright (c) 1982, 2018, Oracle. All rights reserved.
Password? (**********?) ******
Connected to:
Oracle Database 12c Enterprise Edition Release 12.2.0.1.0 - 64bit Production
SQL> @uninstall

## 2.18 About HTTP Error Responses

You may configure ORDS to generate HTTP error responses exclusively in `HTML` or `JSON` format (the default setting is "Auto"). You can modify the error response format by issuing the following ORDS CLI commands:

| Format | Command |
| ------ | ------- |
| HTML   | `ords config set error.responseFormat html` |
| JSON   | `ords config set error.responseFormat json` |
| Auto (*default*) | `ords config set error.responseFormat auto`|  

After issuing one of the above commands two things will occur:

1. The ORDS CLI will respond with a message that your configuration setting has been updated.
2. Any `pool.xml` files associated with this ORDS installation will automatically update to reflect the changes.
3. The following images illustrate these changes:
   - HTML  
   ![error-response-format-auto](./images/error-response-confirmation-html.png " ")  
   ![error-response-format-auto](./images/pool-error-response-html.png " ")
   - JSON  
   ![error-response-format-auto](./images/error-response-confirmation-json.png " ")  
   ![error-response-format-auto](./images/pool-error-response-json.png " ")  
   - Auto  
   ![error-response-format-auto](./images/error-response-confirmation-auto.png " ")  
   ![error-response-format-auto](./images/pool-error-response-auto.png " ")

> **NOTE:** Prior to ORDS 20.4, only `HTML` responses were supported. To preserve this backward compatibility, by default (i.e., via the Auto setting), ORDS attempts to automatically determine the best format to render error responses.

### 2.18.1 About the error.responseFormat

The `error.responseFormat` setting is a *global*[^1] setting that supports the following values:

- `HTML` - error responses are returned in `HTML` format.
- `JSON` - error responses are returned in `JSON` format.
- `Auto` (*default setting*) - Automatically determines the most appropriate format for error responses.

You may use the following ORDS command line command to review your existing configuration settings:

```sh
ords config list --include-defaults
```

![error-response-format-auto](./images/ords-config-list-include-defaults.png " ")

> [^1]: Global settings are those settings found in the `/[your ORDS configuration folder]/global/settings.xml` file. These settings apply to all ORDS instances, regardless of whether they are installed at the Container database (CDB) or Pluggable database (PDB) level.
>
> **NOTE:** An ORDS best practice is to install ORDS at the *PDB level*. This configuration supports High-Availability, Fast Failover, rolling updates, etc. See our Best Practices page for [more details](https://www.oracle.com/database/technologies/appdev/rest/best-practices/).

#### 2.18.1.1 `HTML` Mode

![error-response-format-html](./images/error-response-format-html.png " ")

ORDS will render error responses in `HTML` format when you set the `error.responseFormat` value to `html`. You may use this setting to match the behavior of ORDS 20.3.1 and prior releases. The HTML format displays properly in web browsers. However, the HTML format is verbose for non-human clients and may be challenging to parse. The JSON format may be a better alternative for these applications.

#### 2.18.1.2 `JSON` Mode

![error-response-format-json](./images/error-response-format-json.png " ")

ORDS will render error responses in `JSON` format when you set the `error.responseFormat` value to `json`. The `JSON` format complies with the Problem Details for HTTP APIs standard[^2].

While the `JSON` format may not display correctly in browsers and can be challenging for non-technical users to decipher. Meanwhile *it is* terse and straightforward for non-human clients to parse. An exception to this may be in a command line environment; tools such as curl[^3] make inspecting JSON simple.

> [^2]: *Learn more* [RFC 7807 Problem Details for HTTP APIs](https://datatracker.ietf.org/doc/html/rfc7807) 
> [^3]: [Download curl](https://curl.se)

#### 2.18.1.3 Auto Mode

![error-response-format-json](./images/error-response-format-auto.png " ")

The default value for ORDS' `error.responseFormat` setting is `auto`. When `auto` is selected, ORDS automatically applies rules according to various conditions and returns responses in the appropriate format. The following conditions and their dispositions are below:

##### `HTML`

The `HTML` format will be returned when the client supplies an...

- `Accept` request header where `text/html` is the "most preferred" media type.[^4]
- `Origin` header *and* request method is a `POST` *and* `Content-Type` is `application/x-www-form-urlencoded`.

##### `JSON`

The `JSON` format will be returned when the client supplies an...

- `Accept` request header and `application/json` or `application/problem+json` is the "most preferred" media type.[^4]
- `X-Requested-With` request header.[^5],[^6]
- `User-Agent` header whose value starts with `curl/`.
- `Origin` request header.[^5]
  - ***EXCEPTION:** Responses will be rendered in the `HTML` format when the request method is `POST` and `Content-Type` is `application/x-www-form-urlencoded`.*

> [^4]: [About q-factor weighting](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Accept#directives).
> [^5]: The presence of this header indicates the request was initiated via JavaScript code. Accordingly, `JSON` is the most appropriate response format.
> [^6]: When performing an asynchronous HTTP (Ajax) request, the header `X-Requested-With: XMLHttpRequest` is always added. [See Settings > headers for details](https://api.jquery.com/jQuery.ajax/#jQuery-ajax-settings).

