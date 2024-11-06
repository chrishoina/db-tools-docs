<!-- pandoc 3-implicit-parameters.md -f markdown -t docx -o 3-implicit-parameters.md.docx -->

# 3 Implicit Parameters

This chapter describes the implicit parameters used in REST service handlers that are not explicitly declared. Oracle REST Data Services (ORDS) adds these parameters automatically to the resource handlers.

ORDS also supports, under certain conditions, automatic binding of the following:

- Query parameters
- Form data
- JSON objects

When query parameters are provided, they are always automatically bound by Resource Handlers. Whereas automatic binding behavior of form data and `JSON` objects are dependent on the following two factors:

1. Where and how the `:body`, `:body_text`, and `:body_json` implicit parameters are used, *and*
2. The media- or MIME type used:
   - `application/x-www-form-urlencoded`
   - `application/json`
   - `multipart/form-data` *with a single file*
   - `multipart/form-data` *with multiple files*

> **NOTE:** Sections **3.1.1 About the :body parameter**, **3.1.2 About the :body_text parameter**, and **3.1.3 About the :body_json parameter** will cover in detail automatic binding behavior under various conditons.

## 3.1 List of Implicit Parameters

The following table lists the implicit parameters:

Note:Parameter names are case sensitive. For example, :CURRENT_USER is not a valid implicit parameter.

Table 3-1 List of Implicit Parameters

| Name | Type | Access Mode | HTTP Header | Description | Introduced |
| ---  | ---  | ------      | -------     | -------     | -------    |
| :body | BLOB | IN | N/A | Specifies the body of the request as a temporary BLOB. | 2.0 |
| :body_text | CLOB | IN | N/A | Specifies the body of the request as a temporary CLOB. | 18.3 |
| :body_json | CLOB | IN | N/A | Specifies the body of the request as a temporary CLOB in JSON format. | 24.1 |
| :content_type | VARCHAR |IN | Content-Type | Specifies the MIME type of the request body, as indicated by the Content-Type request header. | 2.0 |
| :current_user | VARCHAR | IN | N/A | Specifies the authenticated user for the request. If no user is authenticated, then the value is set to null. | 2.0 |
| :forward_location | VARCHAR | OUT | X-ORDS-FORWARD-LOCATION | Specifies the location where Oracle REST Data Services must forward a GET request to produce the response for this request. | 18.3 |
| :fetch_offset | NUMBER | IN | N/A | Specifies the zero-based offset of the first row to be displayed on a page. | 18.3 |
| :fetch_size | NUMBER | IN | N/A | Specifies the maximum number of rows to be retrieved on a page. | 18.3 |
| :page_offset | NUMBER | IN | N/A | Specifies the zero based page offset in a paginated request. Note: The :page_offset parameter is deprecated. Use :row_offset parameter instead. | 2.0 |
| :page_size | NUMBER | IN | N/A | Specifies the maximum number of rows to be retrieved on a page. Note: The :page_size parameter is deprecated. Use :fetch_size parameter instead. | 2.0 |
| :row_offset | NUMBER | IN | N/A | Specifies the one-based index of the first row to be displayed in a paginated request. | 3.0 |
| :row_count | NUMBER | IN | N/A | Specifies the one-based index of the last row to be displayed in a paginated request. | 3.0 |
| :status_code | NUMBER | OUT | X-ORDS-STATUS-CODE | Specifies the HTTP status code for the request. | 18.3 |

### 3.1.3 About the :body_json parameter

The `:body_json` implicit parameter can be used with `POST` Resource Handlers to receive the contents of the request body as JSON object. This allows Resource Handlers to directly reference JSON properties (i.e., `{"key": "value"}` pairs).[^1]

Additionally, the `:body_json` implicit parameter can be used when form data and one or more files are included in `multipart/form-data` `POST` requests. Form data, bound to the `:body_json` implicit parameter, continues to be received as a `JSON` object while [one or more] files can be processed with the `ORDS.BODY_FILE_COUNT LOOP` function and the `ORDS.GET_BODY_FILE` procedure.

> [^1]: In a scenario such as this, the form data in the `POST` body is formatted as a `JSON` object,  and treated as a CLOB data type in the Oracle database. While *you can* store `JSON` in the Oracle database as `JSON`, `VARCHAR2`, `CLOB`, and `BLOB`, ORDS uses the `CLOB` data type, to ensure backward compatibility with earlier releases of the Oracle database.

Similar to the `:body` and `:body_text` implicit parameters, when the`:body_json` implicit parameter is included in a Resource Handler, *it must be invoked* in order to be used. The `:body_json` parameter can be invoked in various ways, such as:

- The `DBMS_OUTPUT` package such as `dbms_output.put_line(:body_json);`
- The hypertext procedures (htp) and functions (htf) packages, such as in `htp.print(:body_json);`
- Assigning the `:body_json` implicit parameter as variable, e.g. l_body_json `:= :body_json;`

#### Scenarios for using :body_json

The below table summarizes the possible scenarios where the `:body_json` implicit parameter can be used. When form data in the `POST` body request is to be received as a `JSON` object, the `:body_json` implicit parameter should be used for the MIME types seen below. Pay special attention to the `multipart/form-data` request in cases where you intend to send 1 or more files in a request.

<!-- |`POST` body contents || Form data (when in `x-www-form-urlencoded` format) | Form data (as `JSON` object) | ≥ 1 file/s |
| :--:| :--: | :--------: | :---: | :---: |
||`application/x-www-form-urlencoded`| - | `:body_json` | - |
| MIME Types |`application/json` | - |`:body_json`| - |
||`multipart/form-data` | - | `:body_json` | `ORDS.BODY_FILE_COUNT LOOP` & `ORDS.GET_BODY_FILE`| -->

<table style="text-align:center">
  <thead>
    <tr style="border-top:none">
      <th scope="col" style="border-style: hidden;"></th>
      <th scope="col" style="border-top: hidden;"></th>
      <th colspan="3" scope="col" style="text-align:center">MIME type</th>
    </tr>
  </thead>
  <tbody>
    <th scope="col" style="border-left-style: hidden;"></th>
      <th scope="row" style="border-left-style:hidden;border-top:hidden;"></th>
      <td><code>application/x-www-form-urlencoded</code></td>
      <td><code>application/json</code></td>
      <td><code>multipart/form-data</code></td>
    </tr>
    <tr>
    <th scope="col" rowspan="3" style="text-align:center"><code>POST</code> body contents</th>
      <td>Form data (when in <code>x-www-form-urlencoded</code> format)</td>
      <td style="text-align:center">-</td>
      <td style="text-align:center">-</td>
      <td style="text-align:center">-</td>
    </tr>
    <tr>
      <td>Form data (as <code>JSON</code> object)</td>
      <td><code>:body_json</code></td>
      <td><code>:body_json</code></td>
      <td><code>:body_json</code></td>
    </tr>
    <tr>
      <td> ≥ 1 file/s included</td>
      <td style="text-align:center">-</td>
      <td style="text-align:center">-</td>
      <td><code>ORDS.BODY_FILE_COUNT LOOP</code>& <code>ORDS.GET_BODY_FILE</code></td>
    </tr>
  </tbody>
</table>

#### Example

A table (`DEMO_TABLE`) has been created with the following attributes:

```sql
CREATE TABLE DEMO_TABLE 
    ( 
     ID              NUMBER (*,0) GENERATED BY DEFAULT AS IDENTITY 
        ( START WITH 1 CACHE 20 )  NOT NULL , 
     FILE_NAME       VARCHAR2 (200) , 
     FILE_BODY       BLOB , 
     CONTENT_TYPE    VARCHAR2 (200) , 
     FILE_VISIBILITY VARCHAR2 (10) , 
     SUBMITTED_BY    VARCHAR2 (200) , 
     SUBMITTED_ON    TIMESTAMP DEFAULT systimestamp.
     SHAPE           VARCHAR2 (20)
    ) 
    TABLESPACE DATA 
    LOGGING 
;
```

> **NOTE:** Columns such as `FILE_VISIBILITY`, `SUBMITTED_BY`, and `SUBMITTED_ON` are for *demonstration purposes only*. They are not required.

An ORDS Endpoint has been created (with the below Resource Handler code). The following conditions exist:

- The endpoint expects multiple files and form data *in a `JSON` format* (i.e., the use of the `:body_json` implicit parameter).
- The `ORDS.BODY_FILE_COUNT` function will be used to count the total files of the `POST` request.
- The `ORDS.GET_BODY_FILE` procedure will be used to store, in session, these files.

The following code example then performs an `INSERT` on the `DEMO_TABLE` and relies upon various HTP procedures to "print" the results to a user, client, or application.

```sql
DECLARE
    L_PARAMETER_NAME VARCHAR2(4000);
    L_FILE_NAME      VARCHAR2(4000);
    L_CONTENT_TYPE   VARCHAR2(200);
    L_FILE_BODY      BLOB;
    L_BODY_JSON      CLOB;
BEGIN
    L_BODY_JSON := :BODY_JSON;
    HTP.PARAGRAPH;
    HTP.PRINT('Submitted By: ' || JSON_VALUE(L_BODY_JSON, '$.submitted_by'));
    HTP.BR;
    HTP.PARAGRAPH;
    HTP.PRINT('File visibility status: ' || JSON_VALUE(L_BODY_JSON, '$.file_visibility'));
    HTP.BR;
    HTP.PARAGRAPH;
    HTP.PRINT('Shape: ' || :SHAPE);
    FOR I IN 1..ORDS.BODY_FILE_COUNT LOOP
        ORDS.GET_BODY_FILE(
            P_FILE_INDEX     => I,
            P_PARAMETER_NAME => L_PARAMETER_NAME,
            P_FILE_NAME      => L_FILE_NAME,
            P_CONTENT_TYPE   => L_CONTENT_TYPE,
            P_FILE_BLOB      => L_FILE_BODY
        );
        INSERT INTO DEMO_TABLE (
            FILE_NAME,
            FILE_BODY,
            CONTENT_TYPE,
            FILE_VISIBILITY,
            SUBMITTED_BY,
            SHAPE
        ) VALUES ( L_FILE_NAME,
                   L_FILE_BODY,
                   L_CONTENT_TYPE,
                   JSON_VALUE(L_BODY_JSON, '$.submitted_by'),
                   JSON_VALUE(L_BODY_JSON, '$.file_visibility'),
                   :shape );
        HTP.PARAGRAPH;
        HTP.PRINT('Inserted File: ' || L_FILE_NAME);
        HTP.BR;
    END LOOP;
END;
```

To test this `:body_json` implicit parameter a curl command such as the one below may be used:

> **NOTE:** You may have observed the included query parameter in the above `POST` request. In this example, we illustrate how automatic binding of query parameters (e.g., `shape=triangle` can be used in ORDS `POST` Resource Handlers).

```shell
curl --location 'https://gf641ea24ecc468-ordsdemo.adb.us-ashburn-1.oraclecloudapps.com/ords/ordsdemo/demo_api/demo?shape=triangle' \
--form 'files=@"demo-3.sql"' \
--form 'files=@"demo-2.sql"' \
--form 'submitted_by="chris"' \
--form 'file_visibility="public"'
```

Accordingly, a client may respond with the following:

```html
<p>
Submitted By: chris
<br />
<p>
File visibility status: public
<br />
<p>
Shape: triangle
<p>
Inserted File: demo-3.sql
<br />
<p>
Inserted File: demo-2.sql
<br />
```

Along with an update to target the `DEMO_TABLE`:

| ID   | FILE_NAME  | FILE_BODY | CONTENT_TYPE     | FILE_VISIBILITY | SUBMITTED_BY | SUBMITTED_ON                 | SHAPE     |
| :--: | :--------: | :-------: | :--------------: | :------------:  | :----------: | :--------------------------: | :--------:|
| 144  | demo-2.sql | (BLOB)    | application/x-sql | public         | chris        | 2024-11-06T15:00:46.494488Z  | triangle  |
| 145  | demo-3.sql | (BLOB)    | application/x-sql | public         | chris        | 2024-11-06T15:00:46.49574Z   | triangle  |
