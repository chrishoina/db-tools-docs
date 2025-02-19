# 8 ORDS_SECURITY PL/SQL Package Reference

## 8.1 JWT Profile actions

### 8.1.1 Create an OAuth2.0 JWT Profile

#### Format

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

#### Description

This procedure creates an OAuth2 JWT Profile for *your* schema.[^8.1.1] The profile is used to validate JWTs, as well as validate that the `subject` property in the JWT has the appropriate scope (as defined in the related ORDS privilege) for this schema.

[^8.1.1]: Test

#### Parameters

| Parameter | Description | Notes |
| --------- | ----------- | ----- |
| `p_issuer` |The issuer of acceptable JWT access tokens. This value must match the "iss" claim provided in the JWT.||
| `p_audience` | The audience of acceptable JWT access tokens. This value must match the "aud" claim provided in the JWT.||
| `p_jwk_url`| This is the url to the jwk(s) used to validate acceptable JWT access tokens. It must start with "https://"|||
| `p_description`| A description of the JWT Profile.| - *Optional*|
| `p_allowed_skew` |The number of seconds allowed to skew time claims provided in the JWT.|- *Optional*<p></p>- Defaults to 0 &nbsp;&nbsp;&nbsp;secs|
| `p_allowed_age` |The maximum allowed age  of a JWT in seconds, regardless of  expired claim.|- *Optional*<p></p>- Default to 0 &nbsp;&nbsp;&nbsp;secs|

#### Usage Notes

#### Examples

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

### Delete an OAuth2.0 JWT Profile

/**
   * Delete a JWT Profile associated with this schema.
   */
  PROCEDURE delete_jwt_profile;

#### Examples

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

## OAuth2.0 Client actions

### Delete an OAuth2.0 Client registration

/**
   * Delete an OAuth client registration.
   *
   * @param p_client_key The key (id|name|client_id) of the client to be deleted
   *                     A minimum of one key must be supplied.
   */
  PROCEDURE delete_client(
      p_client_key IN ords_types.t_client_key
  );

  /**
   * Delete an OAuth client registration.
   *
   * @param p_name The name of the client to be deleted.
   *               This value must not be null
   */
  PROCEDURE delete_client(
      p_name IN VARCHAR
  );

  /**
   * Grant an OAuth client with the specified role.
   *
   *
   * @param p_client_key The key (id|name|client_id) of the client to be deleted
   *                     A minimum of one key must be supplied.
   * @param p_role_name The name of a role that either belongs to the schema or is a built in role.
   *                    This value must must not be null.
   */

### Importing an OAuth2.0 client

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

### Register an OAuth2.0 client

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

### Updating an OAuth2.0 client registration

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

### Verifying an OAuth2.0 ID and secret

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

## OAuth2.0 Client Role and Privilege actions

### Updating OAuth2.0 client privileges

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

### Granting an OAuth2.0 client role

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

## Managing OAuth2.0 Client Secrets

### Generate (Rotate) a new OAuth2.0 secret by client_key

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

### Generate (Rotate) a new OAuth2.0 secret by client name

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

### Revoke an OAuth2.0 client's secret by client_key

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

### Revoke an OAuth2.0 client's secret by client name

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

## Managing OAuth2.0 client tokens

### Updating access token duration for an OAuth2.0 client

#### Updating an OAuth2.0 client's access token duration by client_key

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

#### Updating an OAuth2.0 client's access token duration by client name

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

## Managing an OAuth2.0 client's logo

### Updating an OAuth2.0 client's logo using the client's key

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

### Updating an OAuth2.0 client's logo using the client's name

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