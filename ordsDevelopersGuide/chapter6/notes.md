# 8 ORDS_SECURITY PL/SQL Package Reference

## 8.1 JWT Profile actions

### 8.1.1 Create an OAuth2.0 JWT Profile

#### 8.1.1.1 Format

```sql
PROCEDURE create_jwt_profile(
      p_issuer       IN oauth_jwt_profile.issuer%type,
      p_audience     IN oauth_jwt_profile.audience%type,
      p_jwk_url      IN oauth_jwt_profile.jwk_url%type,
      p_description  IN oauth_jwt_profile.description%type  DEFAULT NULL,
      p_allowed_skew IN oauth_jwt_profile.allowed_skew%type DEFAULT NULL,
      p_allowed_age  IN oauth_jwt_profile.allowed_age%type  DEFAULT NULL
  );
```

#### 8.1.1.2 Description

This procedure creates an OAuth2 JWT Profile for *your* schema.[^8.1.1.1.2] The profile is used to validate JWTs, as well as validate that the `subject` property in the JWT has the appropriate scope (as defined in the related ORDS privilege) for this schema.

[^8.1.1.1.2]: As the ADMIN user, you can create JWT Profiles for other users (Schemas). In order to do this, you'll need to refer to the `CREATE_JWT_PROFILE` procedure in the `ORDS_SECURITY_ADMIN` PL/SQL Package.

#### 8.1.1.3 Parameters

| Parameter | Description | Notes |
| --------- | ----------- | ----- |
| `p_issuer` |The issuer of acceptable JWT access tokens. This value must match the "iss" claim provided in the JWT.||
| `p_audience` | The audience of acceptable JWT access tokens. This value must match the "aud" claim provided in the JWT.||
| `p_jwk_url`| This is the url to the jwk(s) used to validate acceptable JWT access tokens. It must start with "https://"|||
| `p_description`| A description of the JWT Profile.| - *Optional*|
| `p_allowed_skew` |The number of seconds allowed to skew time claims provided in the JWT.|- *Optional*<p></p>- Defaults to 0 &nbsp;&nbsp;&nbsp;secs|
| `p_allowed_age` |The maximum allowed age  of a JWT in seconds, regardless of  expired claim.|- *Optional*<p></p>- Default to 0 &nbsp;&nbsp;&nbsp;secs|

> :bulb: **Tip:** You can review existing a JWT Profile with the `USER_ORDS_JWT_PROFILE` View. Use the following SQL query `SELECT * USER_ORDS_JWT_PROFILE;`, or fully-qualified version `SELECT * FROM ORDS_METADATA.USER_ORDS_JWT_PROFILE;`.

#### 8.1.1.4 Usage Notes

If a JWT profile already exists, then it must be deleted first. For this operation to take effect,
include the `COMMIT` statement after calling the `ORDS_SECURITY.DELETE_JWT_PROFILE;` procedure. 

You can execute this procedure seperately or from with the same block as the `ORDS_SECURITY.CREATE_JWT_PROFILE;` procedure.

*Executing the `ORDS_SECURITY.DELETE_JWT_PROFILE;` separately*

```sql
BEGIN
    ORDS_SECURITY.DELETE_JWT_PROFILE();
    COMMIT;
END;

```

*As a simple `EXECUTE` command:*

```sql
EXECUTE ORDS_SECURITY.DELETE_JWT_PROFILE;
COMMIT;
```

*Including in the same block as the `CREATE_JWT_PROFLE` procedure.*

```sql
BEGIN
    ORDS_SECURITY.DELETE_JWT_PROFILE;
    ORDS_SECURITY.CREATE_JWT_PROFILE(
    p_issuer => 'https://identity.oraclecloud.com/',
    p_audience => 'ords/myapplication/api' ,
    p_jwk_url =>'https://
    idcs-10a10a10a10a10a10a10a10a.identity.oraclecloud.com/admin/v1/SigningCert/
    jwk'
    );
    COMMIT;
END;
/
```

#### 8.1.1.5 Examples

##### Oracle Identity Access Management

```sql
DECLARE
    L_P_ISSUER       VARCHAR2(200) := 'https://identity.oraclecloud.com/';
    L_P_AUDIENCE     VARCHAR2(200) := 'ords/';
    L_P_JWK_URL      VARCHAR2(200) := 'https://idcs-66de820ed85f41f0805119c5967689b2.identity.oraclecloud.com:443/admin/v1/SigningCert/jwk'
    ;
    L_P_DESCRIPTION  VARCHAR2(200) := 'Example JWT Client Profile';
    L_P_ALLOWED_SKEW NUMBER;
    L_P_ALLOWED_AGE  NUMBER;
BEGIN
    ORDS_METADATA.ORDS_SECURITY.CREATE_JWT_PROFILE(
        P_ISSUER       => L_P_ISSUER,
        P_AUDIENCE     => L_P_AUDIENCE,
        P_JWK_URL      => L_P_JWK_URL,
        P_DESCRIPTION  => L_P_DESCRIPTION,
        P_ALLOWED_SKEW => L_P_ALLOWED_SKEW,
        P_ALLOWED_AGE  => L_P_ALLOWED_AGE
    );
END;
```

##### Microsoft Entra

```sql
BEGIN
    ORDS_METADATA.ORDS_SECURITY.CREATE_JWT_PROFILE(
        P_ISSUER       => https://login.microsoftonline.com/[Your Microsoft Tenancy ID]/v2.0,
        P_AUDIENCE     => '1234abcd-ef56-gh78-ij91-123456abcdefg',
        P_JWK_URL      => 'https://login.microsoftonline.common/discovery/v2.0/keys',
        P_DESCRIPTION  => Example JWT Client Profile
    ); 
END;
```

> :memo: **Note:** Identify providers may differ on how certain parameters should be structured. For example, OCI Identity Access Management uses the Primary Audience of an Integrated Application and requires a trailing slash for the `AUD` claim, whereas Microsoft Entra uses the Application (client) ID as the `AUD` claim. Please refer to your Identity Provider's documentation for guidance on how claims should be structured.

### 8.1.2 Delete an OAuth2.0 JWT Profile

#### 8.1.2.1 Format

`PROCEDURE delete_jwt_profile;`

#### 8.1.2.2 Description

This procedure deletes an existing JWT Profile. Once a JWT profile has been deleted, JWT bearer tokens will no longer be accepted when authorizing requests to those protected resources.

#### 8.1.2.3 Usage notes

For this operation to take effect, use the `COMMIT` statement after calling this method.

#### 8.1.2.4 Examples

*As an PL/SQL Anonymous Block:*

```sql
BEGIN
    ORDS_SECURITY.DELETE_JWT_PROFILE;
COMMIT;
END
```

*As a simple `EXECUTE` command:*

```sql
EXECUTE ORDS_SECURITY.DELETE_JWT_PROFILE;
COMMIT;
```

## 8.2 OAuth2.0 Client actions

### 8.2.1 Delete an OAuth2.0 Client registration

#### 8.2.1.1 Delete an OAuth2.0 Client registration *by `id`*

<!-- Need clarification from Dick on the correct syntax for these. -->
##### 8.2.1.1.1 Format

```sql
PROCEDURE delete_client(
      p_client_key IN ords_types.t_client_key
  );
```

##### 8.2.1.1.2 Description

Deletes an OAuth2.0 client registration using the ID of the client.[^8.2.1.1]

> :memo: **Note:** The ID and the Client ID are different values. The ID of the client is the unique identifer used for functions and identification *within* the database. Whereas the Client ID is the ID that is associated with a registered client application (i.e. the value ususally stored in your application's environment variables file).

[^8.2.1.1]: You can obtain the details of your OAuth2.0 client registrations with the `ORDS_METADATA.USER_ORDS_CLIENTS` ORDS-provided view. Simply execute a `SELECT * FROM ORDS_METADATA.USER_ORDS_CLIENTS;` query to review the details of your client registrations.

##### 8.2.1.1.3 Parameters

##### 8.2.1.1.4 Usage notes

##### 8.2.1.1.5 Examples

```sql
BEGIN
    ORDS_SECURITY.DELETE_CLIENT(
    p_client_key => ords_types.oauth_client_key(p_id => 10604)
    );
COMMIT;
END;
/
```

/**
   * Delete an OAuth client registration.
   *
   * @param p_client_key The key (id|name|client_id) of the client to be deleted
   *                     A minimum of one key must be supplied.
   */
  PROCEDURE delete_client(
      p_client_key IN ords_types.t_client_key
  );

#### 8.2.1.1 Delete an OAuth2.0 Client registration *by `client_id`*

##### Format
##### Description
##### Parameters
##### Usage notes
##### Examples

  /**
   * Delete an OAuth client registration.
   *
   * @param p_name The name of the client to be deleted.
   *               This value must not be null
   */
  PROCEDURE delete_client(
      p_name IN VARCHAR
  );

#### 8.2.1.1 Delete an OAuth2.0 Client registration *by `name`*

##### Format

```sql
PROCEDURE delete_client(
      p_client_key IN ords_types.t_client_key
  );
```

##### Description

Deletes an OAuth2.0 client registration using the ID of the client.[^8.2.1.1]

> :memo: **Note:** The ID and the Client ID are different values. The ID of the client is the unique identifer used for functions and identification *within* the database. Whereas the Client ID is the ID that is associated with a registered client application (i.e. the value ususally stored in your application's environment variables file).

[^8.2.1.1]: You can obtain the details of your OAuth2.0 client registrations with the `ORDS_METADATA.USER_ORDS_CLIENTS` ORDS-provided view. Simply execute a `SELECT * FROM ORDS_METADATA.USER_ORDS_CLIENTS;` query to review the details of your client registrations.

##### Parameters
##### Usage notes

##### Examples

```sql
FROM
    ORDS_METADATA.USER_ORDS_CLIENTS BEGIN
    ORDS_SECURITY.DELETE_CLIENT(p_name => 'testclient');
    COMMIT;
END;
```

  /**
   * Grant an OAuth client with the specified role.
   *
   *
   * @param p_client_key The key (id|name|client_id) of the client to be deleted
   *                     A minimum of one key must be supplied.
   * @param p_role_name The name of a role that either belongs to the schema or is a built in role.
   *                    This value must must not be null.
   */

### 8.2.2 Importing an OAuth2.0 client
<!-- What is the purpose or use case for the import procedure? What are you importing from? -->
/**
   * Import an OAuth client
   *
   * No secret will be registered by the method. Use register_client_secret or
   * rotate_client_secret subsequently to register a secret.
   *
   * @param p_name Human readable name for the client, displayed to the end user
   *               during the approval phase of three-legged OAuth.
   *               This value must not be null
   * @param p_grant_type Must be one of: 'authorization_code', 'implicit' or
   *                     'client_credentials'.
   * @param p_client_id The original generated client identifier @see ORDS_EXPORT
   *                    When null, a new client identifier is generated
   * @param p_privilege_names Names of the privileges that the client wishes to
   *                          access. Each privilege name must be separated by a comma character.
   * @param p_description Human readable description of the purpose of the
   *                      client, displayed to the end user during the
   *                      approval phase of three-legged OAuth. May be null
   *                      if p_grant_type == 'client_credentials', non null
   *                      otherwise.
   * @param p_redirect_uri Client controlled URI to which redirect containing
   *                       OAuth access token/error will be sent. May be null
   *                       if p_grant_type == 'client_credentials', non null
   *                       otherwise.
   * @param p_support_email Support e-mail for client's users
   * @param p_support_uri Support URI for client's users
   * @param p_token_duration   Duration of the access token (bearer) in seconds. Null uses ORDS instance default value
   *                           Which can be set by property or 3600 seconds by default.
   * @param p_refresh_duration Duration of refresh token in seconds.
   *                           Null uses ORDS instance default value set by a property or 86400 seconds.
   * @param p_code_duration    Duration of the code token in seconds (only applicable when grant_type is authorization
   *                           code. If the value is set to null or the grant_type is not authorization_code. The lifetime
   *                           will be the one defined in the ords instance access_token/12 (300 by default).
   * @return The client key (including client_id).
   */
  FUNCTION import_client(
      p_name             IN VARCHAR2,
      p_grant_type       IN VARCHAR2,
      p_description      IN VARCHAR2 DEFAULT NULL,
      p_client_id        IN VARCHAR2 DEFAULT NULL,
      p_privilege_names  IN VARCHAR2 DEFAULT NULL,
      p_origins_allowed  IN VARCHAR2 DEFAULT NULL,
      p_redirect_uri     IN VARCHAR2 DEFAULT NULL,
      p_support_email    IN VARCHAR2 DEFAULT NULL,
      p_support_uri      IN VARCHAR2 DEFAULT NULL,
      p_token_duration   IN NUMBER   DEFAULT NULL,
      p_refresh_duration IN NUMBER   DEFAULT NULL,
      p_code_duration    IN NUMBER   DEFAULT NULL
  ) RETURN ords_types.t_client_key;

  /**
   * Import an OAuth client
   *
   * No secret will be registered by the method. Use register_client_secret or
   * rotate_client_secret subsequently to register a secret.
   *
   * @param p_name Human readable name for the client, displayed to the end user
   *               during the approval phase of three-legged OAuth.
   *               This value must not be null
   * @param p_grant_type Must be one of: 'authorization_code', 'implicit' or
   *                     'client_credentials'.
   * @param p_client_id The original generated client identifier @see ORDS_EXPORT
   *                    When null, a new client identifier is generated
   * @param p_privilege_names Names of the privileges that the client wishes to
   *                          access. Each privilege name must be separated by a comma character.
   * @param p_description Human readable description of the purpose of the
   *                      client, displayed to the end user during the
   *                      approval phase of three-legged OAuth. May be null
   *                      if p_grant_type == 'client_credentials', non null
   *                      otherwise.
   * @param p_redirect_uri Client controlled URI to which redirect containing
   *                       OAuth access token/error will be sent. May be null
   *                       if p_grant_type == 'client_credentials', non null
   *                       otherwise.
   * @param p_support_email Support e-mail for client's users
   * @param p_support_uri Support URI for client's users
   * @param p_token_duration   Duration of the access token (bearer) in seconds. Null uses ORDS instance default value
   *                           Which can be set by property or 3600 seconds by default.
   * @param p_refresh_duration Duration of refresh token in seconds.
   *                           Null uses ORDS instance default value set by a property or 86400 seconds.
   * @param p_code_duration    Duration of the code token in seconds (only applicable when grant_type is authorization
   *                           code. If the value is set to null or the grant_type is not authorization_code. The lifetime
   *                           will be the one defined in the ords instance access_token/12 (300 by default).
   */
  PROCEDURE import_client(
      p_name             IN VARCHAR2,
      p_grant_type       IN VARCHAR2,
      p_description      IN VARCHAR2 DEFAULT NULL,
      p_client_id        IN VARCHAR2 DEFAULT NULL,
      p_privilege_names  IN VARCHAR2 DEFAULT NULL,
      p_origins_allowed  IN VARCHAR2 DEFAULT NULL,
      p_redirect_uri     IN VARCHAR2 DEFAULT NULL,
      p_support_email    IN VARCHAR2 DEFAULT NULL,
      p_support_uri      IN VARCHAR2 DEFAULT NULL,
      p_token_duration   IN NUMBER   DEFAULT NULL,
      p_refresh_duration IN NUMBER   DEFAULT NULL,
      p_code_duration    IN NUMBER   DEFAULT NULL
  );

### 8.2.3 Register an OAuth2.0 client

  /**
   * Register an OAuth client
   *
   * @param p_name Human readable name for the client, displayed to the end user
   *               during the approval phase of three-legged OAuth.
   *               This value must not be null
   * @param p_grant_type Must be one of: 'authorization_code', 'implicit' or
   *                     'client_credentials'.
   * @param p_description Human readable description of the purpose of the
   *                      client, displayed to the end user during the
   *                      approval phase of three-legged OAuth. May be null
   *                      if p_grant_type == 'client_credentials', non null
   *                      otherwise.
   * @param p_client_secret The client secret. Any fields can be set except issued_on.
   *                        (DEFAULT: no secret is registered).
   * @param p_privilege_names Names of the privileges that the client wishes to
   *                          access. Each privilege name must be separated by a comma character.
   * @param p_origins_allowed allowed origins
   * @param p_redirect_uri Client controlled URI to which redirect containing
   *                       OAuth access token/error will be sent. May be null
   *                      if p_grant_type == 'client_credentials', non null
   *                      otherwise.
   * @param p_support_email Support e-mail for client's users
   * @param p_support_uri Support URI for client's users
   * @param p_token_duration Bearer duration in seconds.
   * @param p_refresh_duration Refresh duration in seconds where applicable.
   * @param p_code_duration Code duration in seconds.
   * @return The client key (id|name|client_id) and client_secret, if any, of the registered client
   */
  FUNCTION register_client(
      p_name             IN VARCHAR2,
      p_grant_type       IN VARCHAR2,
      p_description      IN VARCHAR2 DEFAULT NULL,
      p_client_secret    IN ords_types.t_client_secret DEFAULT ords_constants.oauth_client_secret_skip,
      p_privilege_names  IN VARCHAR2 DEFAULT NULL,
      p_origins_allowed  IN VARCHAR2 DEFAULT NULL,
      p_redirect_uri     IN VARCHAR2 DEFAULT NULL,
      p_support_email    IN VARCHAR2 DEFAULT NULL,
      p_support_uri      IN VARCHAR2 DEFAULT NULL,
      p_token_duration   IN NUMBER   DEFAULT NULL,
      p_refresh_duration IN NUMBER   DEFAULT NULL,
      p_code_duration    IN NUMBER   DEFAULT NULL
      ) RETURN ords_types.t_client_credentials;

  /**
   * Register an OAuth client
   *
   * No secret will be registered for this client. Use register_client_secret or
   * rotate_client_secret to register a secret.
   *
   * @param p_name Human readable name for the client, displayed to the end user
   *               during the approval phase of three-legged OAuth.
   *               This value must not be null
   * @param p_grant_type Must be one of: 'authorization_code', 'implicit' or
   *                     'client_credentials'.
   * @param p_description Human readable description of the purpose of the
   *                      client, displayed to the end user during the
   *                      approval phase of three-legged OAuth. May be null
   *                      if p_grant_type == 'client_credentials', non null
   *                      otherwise.
   * @param p_privilege_names Names of the privileges that the client wishes to
   *                          access. Each privilege name must be separated by a comma character.
   * @param p_origins_allowed allowed origins
   * @param p_redirect_uri Client controlled URI to which redirect containing
   *                       OAuth access token/error will be sent. May be null
   *                      if p_grant_type == 'client_credentials', non null
   *                      otherwise.
   * @param p_support_email Support e-mail for client's users
   * @param p_support_uri Support URI for client's users
   * @param p_token_duration Bearer duration in seconds.
   * @param p_refresh_duration Refresh duration in seconds where applicable.
   * @param p_code_duration Code duration in seconds.
   */
  PROCEDURE register_client(
      p_name             IN VARCHAR2,
      p_grant_type       IN VARCHAR2,
      p_description      IN VARCHAR2 DEFAULT NULL,
      p_privilege_names  IN VARCHAR2 DEFAULT NULL,
      p_origins_allowed  IN VARCHAR2 DEFAULT NULL,
      p_redirect_uri     IN VARCHAR2 DEFAULT NULL,
      p_support_email    IN VARCHAR2 DEFAULT NULL,
      p_support_uri      IN VARCHAR2 DEFAULT NULL,
      p_token_duration   IN NUMBER   DEFAULT NULL,
      p_refresh_duration IN NUMBER   DEFAULT NULL,
      p_code_duration    IN NUMBER   DEFAULT NULL
      );

### 8.2.4 Updating an OAuth2.0 client registration

/**
   * Update an OAuth client registration.
   *
   * @param p_client_key The key (id|name|client_id) of the client to be modified.
   *                     A minimum of one key must be supplied.
   * @param p_new_name Human readable name for the client, displayed to the end user
   *                   during the approval phase of three-legged OAuth.
   *                   When null, the old name is preserved.
   * @param p_description Human readable description of the purpose of the
   *                      client, displayed to the end user during the
   *                      approval phase of three-legged OAuth. May be null
   *                      if p_grant_type == 'client_credentials', non null
   *                      otherwise.
   * @param p_origins_allowed allowed origins
   * @param p_redirect_uri Client controlled URI to which redirect containing
   *                       OAuth access token/error will be sent. May be null
   *                      if p_grant_type == 'client_credentials', non null
   *                      otherwise.
   * @param p_support_email Support e-mail for client's users
   * @param p_support_uri Support URI for client's users
   * @return The client key (id|name|client_id) of the updated client.
   */
  FUNCTION update_client(
      p_client_key      IN ords_types.t_client_key,
      p_new_name        IN VARCHAR2 DEFAULT NULL,
      p_description     IN VARCHAR2,
      p_origins_allowed IN VARCHAR2,
      p_redirect_uri    IN VARCHAR2,
      p_support_email   IN VARCHAR2,
      p_support_uri     IN VARCHAR2
  ) RETURN ords_types.t_client_key;

  /**
   * Update an OAuth client registration.
   *
   * @param p_name The name of the client to be modified.
   *               This value must not be null.
   * @param p_new_name Human readable name for the client, displayed to the end user
   *                   during the approval phase of three-legged OAuth.
   *                   When null, the old name is preserved.
   * @param p_description Human readable description of the purpose of the
   *                      client, displayed to the end user during the
   *                      approval phase of three-legged OAuth. May be null
   *                      if p_grant_type == 'client_credentials', non null
   *                      otherwise.
   * @param p_origins_allowed allowed origins
   * @param p_redirect_uri Client controlled URI to which redirect containing
   *                       OAuth access token/error will be sent. May be null
   *                      if p_grant_type == 'client_credentials', non null
   *                      otherwise.
   * @param p_support_email Support e-mail for client's users
   * @param p_support_uri Support URI for client's users
   */
  PROCEDURE update_client(
      p_name            IN VARCHAR2,
      p_new_name        IN VARCHAR2 DEFAULT NULL,
      p_description     IN VARCHAR2,
      p_origins_allowed IN VARCHAR2,
      p_redirect_uri    IN VARCHAR2,
      p_support_email   IN VARCHAR2,
      p_support_uri     IN VARCHAR2
  );

  /**
   * Update an OAuth client registration.
   *
   * @param p_client_key The key (id|name|client_id) of the client to be modified.
   *                     A minimum of one key must be supplied.
   * @param p_new_name Human readable name for the client, displayed to the end user
   *                   during the approval phase of three-legged OAuth.
   *                   When null, the old name is preserved.
   * @param p_description Human readable description of the purpose of the
   *                      client, displayed to the end user during the
   *                      approval phase of three-legged OAuth. May be null
   *                      if p_grant_type == 'client_credentials', non null
   *                      otherwise.
   * @param p_privilege_names Names of the privileges that the client wishes to
   *                          access. Each privilege name must be separated by a comma character.
   * @param p_origins_allowed allowed origins
   * @param p_redirect_uri Client controlled URI to which redirect containing
   *                       OAuth access token/error will be sent. May be null
   *                      if p_grant_type == 'client_credentials', non null
   *                      otherwise.
   * @param p_support_email Support e-mail for client's users
   * @param p_support_uri Support URI for client's users
   * @param p_token_duration   Duration of the access token (bearer) in seconds. Null uses ORDS instance default value
   *                           Which can be set by property or 3600 seconds by default.
   * @param p_refresh_duration Duration of refresh token in seconds.
   *                           Null uses ORDS instance default value set by a property or 86400 seconds.
   * @param p_code_duration    Duration of the code token in seconds (only applicable when grant_type is authorization
   *                           code. If the value is set to null or the grant_type is not authorization_code. The lifetime
   *                           will be the one defined in the ords instance access_token/12 (300 by default).
   * @return The client key (id|name|client_id) of the updated client.
   */
  FUNCTION update_client(
      p_client_key       IN ords_types.t_client_key,
      p_new_name         IN VARCHAR2 DEFAULT NULL,
      p_description      IN VARCHAR2,
      p_privilege_names  IN VARCHAR2,
      p_origins_allowed  IN VARCHAR2,
      p_redirect_uri     IN VARCHAR2,
      p_support_email    IN VARCHAR2,
      p_support_uri      IN VARCHAR2,
      p_token_duration   IN NUMBER,
      p_refresh_duration IN NUMBER,
      p_code_duration    IN NUMBER
  ) RETURN ords_types.t_client_key;

  /**
   * Update an OAuth client registration.
   *
   * @param p_name The name of the client to be modified.
   *               This value must not be null.
   * @param p_new_name Human readable name for the client, displayed to the end user
   *                   during the approval phase of three-legged OAuth.
   *                   When null, the old name is preserved.
   * @param p_description Human readable description of the purpose of the
   *                      client, displayed to the end user during the
   *                      approval phase of three-legged OAuth. May be null
   *                      if p_grant_type == 'client_credentials', non null
   *                      otherwise.
   * @param p_privilege_names Names of the privileges that the client wishes to
   *                          access. Each privilege name must be separated by a comma character.
   * @param p_origins_allowed allowed origins
   * @param p_redirect_uri Client controlled URI to which redirect containing
   *                       OAuth access token/error will be sent. May be null
   *                      if p_grant_type == 'client_credentials', non null
   *                      otherwise.
   * @param p_support_email Support e-mail for client's users
   * @param p_support_uri Support URI for client's users
   * @param p_token_duration   Duration of the access token (bearer) in seconds. Null uses ORDS instance default value
   *                           Which can be set by property or 3600 seconds by default.
   * @param p_refresh_duration Duration of refresh token in seconds.
   *                           Null uses ORDS instance default value set by a property or 86400 seconds.
   * @param p_code_duration    Duration of the code token in seconds (only applicable when grant_type is authorization
   *                           code. If the value is set to null or the grant_type is not authorization_code. The lifetime
   *                           will be the one defined in the ords instance access_token/12 (300 by default).
   */
  PROCEDURE update_client(
      p_name             IN VARCHAR2,
      p_new_name         IN VARCHAR2 DEFAULT NULL,
      p_description      IN VARCHAR2,
      p_privilege_names  IN VARCHAR2,
      p_origins_allowed  IN VARCHAR2,
      p_redirect_uri     IN VARCHAR2,
      p_support_email    IN VARCHAR2,
      p_support_uri      IN VARCHAR2,
      p_token_duration   IN NUMBER,
      p_refresh_duration IN NUMBER,
      p_code_duration    IN NUMBER
  );

### 8.2.5 Verifying an OAuth2.0 ID and secret

/**
   * Verifies the client identifier and secret
   *
   * Returns null if the client is invalid
   * Returns a cursor of rolls the client exists in the caller context and the
   * id and secret are valid.
   *
   * @param p_client_id The OAuth Client Identifier
   * @param p_client_secret The OAuth Client Secret
   * @return A cursor of the assigned roles or null is not verified.
   */
  FUNCTION verify_client(
      p_client_id     IN VARCHAR2,
      p_client_secret IN VARCHAR2 DEFAULT NULL
  ) RETURN sys_refcursor;
END ORDS_SECURITY;

## 8.3 OAuth2.0 Client Role and Privilege actions

### 8.3.1 Updating OAuth2.0 client privileges

/**
   * Updates the OAuth client privileges
   *
   * @param p_client_key The key (id|name|client_id) of the client to be modified.
   *                     A minimum of one key must be supplied.
   * @param p_privilege_names Names of the privileges that the client wishes to
   *                          access. Each privilege name must be separated by a comma character.
   */
  PROCEDURE update_client_privileges(
      p_client_key      IN ords_types.t_client_key,
      p_privilege_names IN VARCHAR2
  );

  /**
   * Updates the OAuth client privileges
   *
   * @param p_name The name of the client to be modified.
   *               This value must not be null.
   * @param p_privilege_names Names of the privileges that the client wishes to
   *                          access. Each privilege name must be separated by a comma character.
   */
  PROCEDURE update_client_privileges(
      p_name            IN VARCHAR2,
      p_privilege_names IN VARCHAR2
  );

### 8.3.2 Granting an OAuth2.0 client role

/**
   * Grant an OAuth client with the specified role.
   *
   *
   * @param p_client_key The key (id|name|client_id) of the client to be deleted
   *                     A minimum of one key must be supplied.
   * @param p_role_name The name of a role that either belongs to the schema or is a built in role.
   *                    This value must must not be null.
   */
  PROCEDURE grant_client_role(
      p_client_key IN ords_types.t_client_key,
      p_role_name  IN VARCHAR2
  );

  /**
   * Grant an OAuth client with the specified role.
   *
   *
   * @param p_client_name The name of the client.
   *                      This value must not be null
   * @param p_role_name The name of a role that either belongs to the schema or is a built in role.
   *                    This value must must not be null.
   */
  PROCEDURE grant_client_role(
      p_client_name IN VARCHAR2,
      p_role_name   IN VARCHAR2
  );

/**
   * Revoke the specified role from an OAuth client, preventing
   * it accessing Privileges requiring the role via two-legged OAuth
   *
   * @param p_client_key The key (id|name|client_id) of the client in the schema.
   *                     A minimum of one key must be supplied.
   * @param p_role_name The name of a role that was previously granted.
   *                    This value must must not be null.
   */
  PROCEDURE revoke_client_role(
      p_client_key IN ords_types.t_client_key,
      p_role_name  IN VARCHAR2);

  /**
   * Revoke the specified role from an OAuth client, preventing
   * it accessing Privileges requiring the role via two-legged OAuth
   *
   * @param p_client_name The name of the client.
   *                      This value must not be null
   * @param p_role_name The name of a role that was previously granted.
   *                    This value must must not be null.
   */
  PROCEDURE revoke_client_role(
      p_client_name IN VARCHAR2,
      p_role_name   IN VARCHAR2);

## 8.4 Managing OAuth2.0 Client Secrets

### 8.4.1 Generate (Rotate) a new OAuth2.0 secret by client_key

/**
   * Generates a new OAuth client secret and, if required, deletes all existing client sessions.
   *
   * If two client secrets are already registerd then the oldest will be overwritten.
   * Any existing client secrets will also remain in effect unless revoked
   * using the p_revoke_existing parameter.
   *
   * IMPORTANT NOTES
   *
   * The generated client secret will not be stored using this method and so requires the caller to
   * save the returned value for future use. The view USER_ORDS_CLIENTS will not return the value either.
   *
   * The view USER_ORDS_CLIENTS cannot return secrets that are not stored.
   *
   * @param p_client_key The key (id|name|client_id) of the client in the schema.
   *                     A minimum of one key must be supplied.
   * @param p_revoke_existing Revokes any exisiting secrets. (Default FALSE)
   * @param p_revoke_sessions Deletes all existing client sessions when TRUE. (Default FALSE)
   * @return The registered client secret value. This value must be saved by the caller for future reference.
   */

  FUNCTION rotate_client_secret(
      p_client_key      IN ords_types.t_client_key,
      p_revoke_existing IN BOOLEAN DEFAULT FALSE,
      p_revoke_sessions IN BOOLEAN DEFAULT FALSE
  ) RETURN ords_types.t_client_credentials;

### 8.4.2 Generate (Rotate) a new OAuth2.0 secret by client name

   /**
    * Generates a new OAuth client secret and, if required, deletes all existing client sessions.
    *
    * If two client secrets are already registerd then the oldest will be overwritten.
    * Any existing client secrets will also remain in effect unless revoked
    * using the p_revoke_existing parameter.
    *
    * IMPORTANT NOTES
    *
    * The generated client secret will not be stored using this method and so requires the caller to
    * save the returned value for future use. The view USER_ORDS_CLIENTS will not return the value either.
    *
    * The view USER_ORDS_CLIENTS cannot return secrets that are not stored.
    *
    * @param p_name The name of the client to be modified.
    *               This value must not be null.
    * @param p_revoke_existing Revokes any exisiting secrets. (Default FALSE)
    * @param p_revoke_sessions Deletes all existing client sessions when TRUE. (Default FALSE)
    * @return The registered client secret value. This value must be saved by the caller for future reference.
    */

   FUNCTION rotate_client_secret(
       p_name            IN VARCHAR2,
       p_revoke_existing IN BOOLEAN DEFAULT FALSE,
       p_revoke_sessions IN BOOLEAN DEFAULT FALSE
  ) RETURN VARCHAR2;

### 8.4.3 Revoke an OAuth2.0 client's secret by client_key

  /**
   * Revoke one or both OAuth client secrets and revokes all sessions when required
   *
   * By default this will only revoke the oldest secret but can be used to revoke one or both secrets
   * through the use of the p_filter parameter. The filter's fields work independently of each other.
   *
   * The special value 3 for the slot number indicated that both slots are to be revoked.
   *
   * @param p_client_key The key (id|name|client_id) of the client.
   *                     A minimum of one key must be supplied.
   * @param p_filter Filter which secret(s) should be revoked.
   *                 When the filter is null then only the oldest secret is revoked.
   *                 When p_filter.slot = 3 then both slots will be revoked.
   *                 When p_filter.stored = FALSE then this only matches when used in isolation.
   * @param p_revoke_sessions Deletes all existing client sessions when TRUE. (Default FALSE)
   * @return The client key (including client_id) and the slot of revoked client_secret of the client
   *         For the returned slot number, a value of 3 indicates that both slots were revoked and
   *         a null value indicated that no slots were revoked. All other client_secret fields are null.
   */
  FUNCTION revoke_client_secrets(
      p_client_key           IN ords_types.t_client_key,
      p_filter               IN ords_types.t_client_secret DEFAULT ords_constants.oauth_client_secret_default,
      p_revoke_sessions      IN BOOLEAN                    DEFAULT FALSE
  ) RETURN ords_types.t_client_credentials;

### 8.4.4 Revoke an OAuth2.0 client's secret by client name

  /**
   * Revoke a OAuth client secret and revokes all sessions when required
   *
   * By default this will only revoke the oldest secret but can be used to revoke one or both secrets
   * if they match the client secret value.
   *
   * @param p_name Human readable name for the client, displayed to the end user
   *               during the approval phase of three-legged OAuth.
   *               This value must not be null
   * @param p_client_secret The value of the client secret. When NULL, the oldest secret is revoked
   * @param p_revoke_sessions Deletes all existing client sessions when TRUE. (Default FALSE)
   */
  PROCEDURE revoke_client_secret(
      p_name            IN VARCHAR2,
      p_client_secret   IN VARCHAR2 DEFAULT NULL,
      p_revoke_sessions IN BOOLEAN  DEFAULT FALSE
  );

## 8.5 Managing OAuth2.0 client tokens

### 8.5.1 Updating access token duration for an OAuth2.0 client

#### 8.5.1.1 Updating an OAuth2.0 client's access token duration by client_key

/**
   * Updates the OAuth client token durations
   *
   * @param p_client_key The key (id|name|client_id) of the client to be modified.
   *                     A minimum of one key must be supplied.
   * @param p_token_duration Bearer duration in seconds.
   * @param p_refresh_duration Refresh duration in seconds where applicable.
   * @param p_code_duration Code duration in seconds.
   */
  PROCEDURE update_client_token_duration(
      p_client_key       IN ords_types.t_client_key,
      p_token_duration   IN NUMBER,
      p_refresh_duration IN NUMBER,
      p_code_duration    IN NUMBER
  );

#### 8.5.1.2 Updating an OAuth2.0 client's access token duration by client name

  /**
   * Updates the OAuth client token durations
   *
   * @param p_name The name of the client to be modified.
   *               This value must not be null.
   * @param p_token_duration Bearer duration in seconds.
   * @param p_refresh_duration Refresh duration in seconds where applicable.
   * @param p_code_duration Code duration in seconds.
   */
  PROCEDURE update_client_token_duration(
      p_name             IN VARCHAR2,
      p_token_duration   IN NUMBER,
      p_refresh_duration IN NUMBER,
      p_code_duration    IN NUMBER
  );

## 8.6 Managing an OAuth2.0 client's logo

### 8.6.1 Updating an OAuth2.0 client's logo using the client's key

  /**
   * Updates the OAuth client logo file
   *
   * @param p_client_key The key (id|name|client_id) of the client to be modified.
   *                     A minimum of one key must be supplied.
   * @param p_content_type The content type of the logo
   * @param p_logo The logo binary
   */
  PROCEDURE update_client_logo(
      p_client_key   IN ords_types.t_client_key,
      p_content_type IN VARCHAR2,
      p_logo         IN BLOB
  );

### 8.6.2 Updating an OAuth2.0 client's logo using the client's name

  /**
   * Updates the OAuth client logo file
   *
   * @param p_name The name of the client to be modified.
   *               This value must not be null.
   * @param p_content_type The content type of the logo
   * @param p_logo The logo binary
   */
  PROCEDURE update_client_logo(
      p_name         IN VARCHAR2,
      p_content_type IN VARCHAR2,
      p_logo         IN BLOB
  );