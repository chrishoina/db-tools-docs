# 3 Implicit Parameters

This chapter describes the implicit parameters used in REST service handlers that are not explicitly declared. Oracle REST Data Services (ORDS) adds these parameters automatically to the resource handlers.

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

### 3.1.1 About the :body parameter

The :body implicit parameter is used in the resource handlers to receive the contents of the request body as a temporary BLOB.

Note:Only POST or PUT requests can have a request body. The HTTP specification does not permit request bodies on GET or DELETE requests.

Example 3-1 Example
The following example illustrates a PL/SQL block that stores the request body in a database table:

begin
 insert into tab (content) values (:body);
end;

Note:

The :body implicit parameter must be dereferenced exactly once in a PL/SQL block. If it is dereferenced more than once, then the second and subsequent dereferences will appear to be empty. This is because the client sends the request body only once. If you need this value more than once, then assign it to a local variable, and dereference the local variable instead.

You can use either one of the implicit parameters :body or :body_text. Otherwise, the PL/SQL block displays an error message "Duplicate steam parameter''.

If you use either :body or :body_text, then you cannot use :bind notation to read attributes of the JSON payload of the request.

The following example will not work as intended because it dereferences the :body parameter twice:

begin
 insert into tab1(content) values (:body); -- request body will be inserted
 insert into tab2(content) values (:body); -- an empty blob will be inserted
end;

To avoid this limitation, the :body parameter value must be assigned to a local PL/SQL variable before it is used. This enables the local variable to be dereferenced more than once:

declare
 l_content blob := :body;
begin
 insert into tabl(content) values(l_content);
 insert into tab2(content) values(l_content);
end;

### 3.1.2 About the :body_text parameter

The :body_text implicit parameter is used in the resource handlers to receive the contents of the request body as a temporary CLOB. Typically, the content of the request body is textual (for example JSON or HTML content) and so, receiving the request body as a CLOB saves the resource handler author from the effort of converting the :body BLOB parameter to a CLOB instance.

Note::body_text implicit parameter must only be dereferenced once inside the entire PL/SQL block. If you need this value more than once, assign it to a local variable, and dereference the local variable instead.

You can use either one of the implicit parameters :body or :body_text. Otherwise, the PL/SQL block displays an error message "Duplicate steam parameter''.

It is recommended to use :body_text ( a character representation ) rather than :body ( a binary representation ) particularly where the PL/SQL block uses JSON functions to process the request body efficiently.

### 3.1.2 About the :body_json parameter

The `:body_json` implicit parameter can be used in Resource Handlers to receive `multipart/form-data` `POST` requests where multiple files are expected to be processed *and* form data should be formatted as a JSON string (*as a CLOB data type*)[^1].

When the`:body_json` implicit parameter is included for Resource Handlers that process multiple files, the `:body_json` implicit parameter must be invoked.
The `:body_json` parameter can be invoked in various ways, such as:

- The `DBMS_OUTPUT` package such as `dbms_output.put_line(:body_json);`
- The hypertext procedures (htp) and functions (htf) packages, such as in `htp.print(:body_json);`
- Assigning the `:body_json` implicit parameter as variable, e.g. l_body_json `:= :body_json;`

> **NOTE:** There is no specific requirement to assign `:body_json` to a local variable. Similarly, there is no requirement to re-use the local variable, should you choose to assign one.

#### Example

A table (`DEMO_TABLE`) has been created with the following attributes:

```sql
CREATE TABLE ORDSDEMO.DEMO_TABLE 
    ( 
     ID              NUMBER (*,0) GENERATED BY DEFAULT AS IDENTITY 
        ( START WITH 1 CACHE 20 )  NOT NULL , 
     FILE_NAME       VARCHAR2 (200) , 
     FILE_BODY       BLOB , 
     CONTENT_TYPE    VARCHAR2 (200) , 
     FILE_VISIBILITY VARCHAR2 (10) , 
     SUBMITTED_BY    VARCHAR2 (200) , 
     SUBMITTED_ON    TIMESTAMP DEFAULT systimestamp 
    ) 
    TABLESPACE DATA 
    LOGGING 
;
```

> **NOTE:** Columns such as `FILE_VISIBILITY`, `SUBMITTED_BY`, and `SUBMITTED_ON` are for *demonstration purposes only*. They are not required.

An ORDS Endpoint has been created (with the below Resource Handler code).

- The endpoint expects multiple files and form data *in a `JSON` format* (i.e., the use of the `:body_json` implicit parameter).
- The `ORDS.BODY_FILE_COUNT` function will be used to count the total files in the `POST` request.
- The `ORDS.GET_BODY_FILE` procedure will be used to store, in session, the files.

The following code example then performs an `INSERT` on the `DEMO_TABLE` and relies upon various HTP procedures to "print" the results to a user, client, or application.

```sql
DECLARE
    L_PARAMETER_NAME  VARCHAR2(4000);
    L_FILE_NAME       VARCHAR2(4000);
    L_CONTENT_TYPE    VARCHAR2(200);
    L_FILE_BODY       BLOB;
    L_FILE_VISIBILITY CLOB;
    L_SUBMITTED_BY    CLOB;
BEGIN
    L_SUBMITTED_BY := JSON_VALUE(:BODY_JSON, '$.submitted_by');
    L_FILE_VISIBILITY := JSON_VALUE(:BODY_JSON, '$.file_visibility');
    HTP.PARAGRAPH;
    HTP.PRINT('Submitted By: ' || L_SUBMITTED_BY);
    HTP.BR;
    HTP.PARAGRAPH;
    HTP.PRINT('File visibility status: ' || L_FILE_VISIBILITY);
    HTP.BR;
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
            SUBMITTED_BY
        ) VALUES ( L_FILE_NAME,
                   L_FILE_BODY,
                   L_CONTENT_TYPE,
                   L_FILE_VISIBILITY,
                   L_SUBMITTED_BY );

        HTP.PARAGRAPH;
        HTP.PRINT('Inserted File: ' || L_FILE_NAME);
    END LOOP;
END;
```

To test this `:body_json` implicit parameter a curl command such as the one below may be used:

```shell
curl --location 'https://localhost:8080/ords/ordsdemo/demo_api/demo' \
--form 'file_one=@"/Users/file_one.txt"' \
--form 'file_two=@"/Users/ile_two.txt"' \
--form 'submitted_by="chris"' \
--form 'file_visibility="public"'
```

Accordingly, a client may respond with the following:

```html
<p>Submitted By: chris
<br />
<p>File visibility status: public
<br />
<p>Inserted File: demo-3.sql
<p>Inserted File: demo-2.sql
```

Along with an update to target `DEMO_TABLE`:

| ID FILE_NAME| FILE_BODY | CONTENT_TYPE | FILE_VISIBILITY | SUBMITTED_BY | SUBMITTED_ON |
| :------------: | :---------: | :------------: | :---------------: | :------------: | :------------: |
| 144          | demo-3.sql | REVDTEFS... | application/x-sql | public | chris |
| 145          | demo-2.sql | Q1JFQVRF... | application/x-sql | public | chris |

<br></br>

> [^1]: Although you can store JSON in the Oracle database as `JSON`, `VARCHAR2`, `CLOB`, and `BLOB`, ORDS uses the `CLOB` data type, to ensure backward compatibility with earlier releases of the Oracle database. 

### 3.1.3 About the :content_type Parameter

The :content_type implicit parameter provides the value of the Content-Type request header supplied with the request. If no Content-Type header is present in the request, then a null value is returned.

### 3.1.4 About the :current_user parameter

The :current_user implicit parameter provides the identity of the user authenticated for the request.

Note:In a scenario, where the user is not authenticated, the value is set to null. For example, if the request is for a public resource, then the value will be set to null.

### 3.1.5 About the :status_code parameter

The :status_code implicit parameter enables a resource handler to indicate the HTTP status code value to include in a response. The value must be one of the numeric values defined in the HTTP Specification document.

### 3.1.6 About the :forward_location parameter

The :forward_location implicit parameter provides a mechanism for PL/SQL based resource handlers to produce a response for a request.

Consider a POST request that results in the creation of a new resource. Typically, the response of a POST request for REST APIs contains the location of the newly created resource (in the Location response header) along with the representation of the new resource. The presence of the Location header in the response indicates that there must be a GET resource handler that can produce a response for the specified location.

Instead of applying logic to the POST resource handler to render the representation of the new resource in the response, the resource handler can delegate that task to the existing GET Resource Handler.

The following resource handler defines a POST handler that delegates the generation of the response to a GET resource handler:

ords.define_handler(
  p_module_name => 'tickets.collection',
  p_pattern => '.',                     
  p_method  => 'POST',
  p_mimes_allowed => 'application/json',
  p_source_type => ords.source_type_plsql,
  p_source => '
   declare
    l_owner varchar2(255);
    l_payload clob;
    l_id number;
   begin
    l_payload := :body_text;
    l_owner := :current_user;
    l_id := ticket_api.create_ticket(
      p_json_entity => l_payload,
      p_author => l_owner
    );
    :forward_location := ''./'' || l_id;
    :status_code := 201;
   end;
  '
);

Where:

    The ords.define_handler API is used to add a POST handler to an existing resource module named tickets.collection.

    The p_pattern with value '.' indicates that the POST handler should be bound to the root resource of the resource module. If the base path of the tickets.collection' is /tickets/, then the POST handler is bound to the /tickets/ URL path.

    The p_mimes_allowed value indicates that the POST request must have a Content-Type header value of application/json'.

    The p_source_type value indicates that the source of the POST handler is a PL/SQL block.

    The p_source value contains the source of the PL/SQL block:

    Where:

    Note:The :body_text implicit parameter is assigned to a local variable, so that it can be dereferenced more than once.

        The identity of the user, making the POST request, is determined from the :current_user implicit parameter.

        The PL/SQL block, delegates the task of storing the request payload to a PL/SQL package level function. The PL/SQL block should only contain logic to bridge from the HTTP request to the PL/SQL package invocation.

        Note:When all the data modification operations are wrapped in a PL/SQL API, the PL/SQL block can be independently unit tested. Long and complicated PL/SQL blocks are an anti-pattern indicative of code that is difficult to test and maintain.

        The PL/SQL package level function returns the ID of the newly created resource.

        The :forward_location implicit parameter is assigned the value of './' || l_id. For example, if the value of l_id is 4256, then the value of :forward_location is /tickets/4256 .

        When ORDS evaluates the preceding PL/SQL block and checks the value assigned to the :forward_location implicit parameter, it initiates a GET request against the specified location (for example, /tickets/4256) and return the response generated by the GET request as the response of the POST request. In addition, ORDS includes a location response header with the fully resolved URL of the :forward_location value.

        The :status_code implicit parameter is assigned the HTTP response status code value. The 201 (Created) status code indicates that a new resource is created. This value will override the status code generated by the GET request.

### 3.1.7 About the pagination implicit parameters

The following table lists the pagination implicit parameters:

Note:Oracle REST Data Services reserves the use of the query parameters, page, offset, and limit. It is not permitted to define REST services that use named bind parameters with any of the preceding query parameter names. Alternatively, REST services must use the appropriate pagination implicit parameters defined in the following table:

Table 3-2 Pagination Implicit Parameters
Name 	Description 	Status

:page_offset
	

Specifies the zero based page offset in a pagination request.
	

Deprecated

:page_size
	

Specifies the maximum number of rows to be retrieved on a page.
	

Deprecated

:row_offset
	

Specifies the index of the first row to be displayed in a pagination request.
	

Not Recommended

:row_count
	

Specifies the index of the last row to displayed in a pagination request.
	

Not Recommended

:fetch_offset
	

Specifies the zero based index of the first row to be displayed on a page.
	

Recommended

:fetch_size
	

Specifies the maximum number of rows to be retrieved on a page.
	

Recommended

#### 3.1.7.1 About the :page_offset parameter

The :page_offset implicit parameter is provided for backward compatibility, so it is used only with source_type_query source type resource handlers.

Note:

    The source_type_query source type is deprecated, instead use the source_type_collection feed parameter.

    The :page_offset implicit parameter is deprecated, instead use the :row_offset implicit parameter.

#### 3.1.7.2 About the :page_size parameter

The :page_size implicit parameter is used to indicate the maximum number of rows to be retrieved on a page. :page_size parameter is provided for backward compatibility. This parameter is deprecated, instead use :fetch_size implicit parameter.

#### 3.1.7.3 About the :row_offset parameter

The :row_offset implicit parameter indicates the number of the first row to be displayed on a page. The :row_offset implicit parameter is used when you are using both a wrapper pagination query and row_number() (used in Oracle 11g and earlier releases). Starting Oracle 12c or later releases, Oracle recommends using the :fetch_offset implicit parameter and a row limiting clause instead of the :row_offset parameter.

#### 3.1.7.4 About the :row_count parameter

The :row_count implicit parameter is used to indicate the number of rows to be displayed on a page. The :row_count value is the value of the sum of :row_offset and the pagination size. The :row_count implicit parameter is useful when implementing pagination using a wrapper pagination query and row_number()method that was used in Oracle database 11g and earlier releases. Starting Oracle Database release 12c or later, Oracle recommends that you use :fetch_size parameter and a row limiting clause instead.

#### 3.1.7.5 About the :fetch_offset parameter

The :fetch_offset implicit parameter is used to indicate the zero based offset of the first row to display in a given page. The :fetch_offset implicit parameter is used when you implement pagination using a row limiting clause, which is recommended for use with Oracle 12c and later releases.

#### 3.1.7.6 About the :fetch_size parameter

The :fetch_size implicit parameter is used to indicate the maximum number of rows to retrieve on a page. ORDS always sets the value of :fetch_size to the pagination size plus one. The presence or absence of the extra row helps ORDS in determining if there is a subsequent page in the results or not.

Note:The extra row that is queried is never displayed on the page.

#### 3.1.7.7 About Automatic pagination

This section describes the automatic pagination process.
If a GET resource handler source type, source_type_collection_feed or source_type_query has a non zero pagination size (p_items_per_page) and the source of the GET resource handler does not dereference any of the implicit pagination parameters discussed in the preceding sections, then ORDS automatically wraps the query in a pagination clause to constrain the query results to include only the values from the requested page. With automatic pagination, the resource handler author needs to specify only the pagination size, and ORDS automatically handles the remaining effort in paginating the resource.

Note:All resource modules have a default pagination size (p_items_per_page) of 25. So, by default automatic pagination is enabled.

#### 3.1.7.8 About Manual pagination

This section describes the manual pagination process.
In some scenarios, a GET resource handler needs to perform pagination on its own rather than delegating the pagination process to ORDS. In such cases, the source of the GET resource handler will dereference one or more implicit pagination parameters discussed in the preceding sections.

Note:The GET resource handler must specify the desired pagination size so that ORDS can correctly calculate the required values for the implicit pagination parameters.

Examples

Manual pagination example using row limiting clause

The following example defines a REST service that uses a row limiting clause to paginate the query result set. This is the recommended way to implement manual pagination:

begin
 ords.define_service(
   p_module_name => 'example.paging',
   p_base_path => '/example/',
   p_pattern => '/paged',
   p_items_per_page => 7,
   p_source => 'select * from emp e order by empno desc offset :fetch_offset rows fetch next :fetch_size rows only'
 );
 commit;
end;

Manual pagination example using row_number() method

The following example defines a REST service that uses a wrapper query and row_number() method. This approach is not recommended.

begin
ords.define_service(
   p_module_name => 'example.paging',
   p_base_path => '/example/',
   p_pattern => '/paged',
   p_items_per_page => 7,
   p_source => 'select * from (select q_.* , row_number() over (order by 1) rn__ from (select * from emp e order by empno desc) q_ )where rn__ between :row_offset and :row_count'
 );
 commit;
end;
