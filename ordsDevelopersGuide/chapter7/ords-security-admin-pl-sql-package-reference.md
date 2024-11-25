<!-- Example pandoc 3-implicit-parameters.md -f markdown -t docx -o 3-implicit-parameters.md.docx -->

<!-- https://oracle-my.sharepoint.com/personal/tulika_das_oracle_com/_layouts/15/onedrive.aspx?csf=1&web=1&e=7EGLVb&CID=a41001e8%2D3a7e%2D403f%2D9234%2D713d44bb73d6&id=%2Fpersonal%2Ftulika%5Fdas%5Foracle%5Fcom%2FDocuments%2FTD%20Projects%2FORDS%20Doc%20Revamp%202023&FolderCTID=0x0120004335BE87777DC644A1BD73BDB63CA75D&view=0 -->

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