# 6 ORDS_Security PL/SQL Package Reference

<!-- Need about section -->

## Create

### JWT Profile

#### Procedures

##### CREATE_JWT_PROFILE

###### Format

```sql
create_jwt_profile(
      p_issuer       IN oauth_jwt_profile.issuer%type,
      p_audience     IN oauth_jwt_profile.audience%type,
      p_jwk_url      IN oauth_jwt_profile.jwk_url%type,
      p_description  IN oauth_jwt_profile.description%type  DEFAULT NULL,
      p_allowed_skew IN oauth_jwt_profile.allowed_skew%type DEFAULT NULL,
      p_allowed_age  IN oauth_jwt_profile.allowed_age%type  DEFAULT NULL
  );
```

###### About

This procedure creates an OAuth2 JWT Profile for the schema.

JWT access tokens which can be validated using this profile, authorize the JWT subject as having the provided scope (ORDS privileges) for this schema.

###### Parameters

| Parameter | Description | Notes |
| --------- | ----------- | ----- |
| `p_issuer` |The issuer of acceptable JWT access tokens. This value must match the "iss" claim provided in the JWT.||
| `p_audience` | The audience of acceptable JWT access tokens. This value must match the "aud" claim provided in the JWT.||
| `p_jwk_url`| This is the url to the jwk(s) used to validate acceptable JWT access tokens. It must start with "https://"|||
| `p_description`| A description of the JWT Profile.| *Optional*|
| `p_allowed_skew` |The number of seconds allowed to skew time claims provided in the JWT.|*Optional*|
| `p_allowed_age` |The maximum allowed age  of a JWT in seconds, regardless of  expired claim.|*Optional*|

## Grant

## Import

## Register

## Rotate

## Revoke

## Update

## Verify 