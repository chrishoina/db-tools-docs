# Oracle REST Data Services Quick Start Guide

## About this tutorial

This tutorial is designed to let you get started quickly developing RESTful services using
Oracle REST Data Services.

## Helpful information

Before you perform the actions in this tutorial, note the following prerequisites and recommendations:

* Ensure that you have Oracle REST Data Services  installed *and* configured for a currently-supported Oracle database
* Ensure that you have installed a currently-supported version of:
  * Oracle SQL Developer
  * SQLcl

> NOTE: The latest version of SQLcl can be obtained [here](https://www.oracle.com/database/sqldeveloper/technologies/sqlcl/download/) *or* through Homebrew with the following `brew install --cask sqlcl` command. Additional SQLcl installation information can be found on [Homebrew](https://formulae.brew.sh/cask/sqlcl#default).

> NOTE: The latest version of Oracle SQL Developer can be obtained [here](https://www.oracle.com/database/sqldeveloper/technologies/download/).

* It is strongly recommended that you install a browser extension that enables you to view
`JSON` in the web browser. Popular browser extensions include:
  * [JSON Formatter](https://chrome.google.com/webstore/detail/json-formatter/bcjindcccaagfpapjjmafapmmgkkhgoa) for Google Chrome
  * [JSONView Add-on](https://addons.mozilla.org/en-US/firefox/addon/jsonview/) for Mozilla Firefox

### This tutorial assumes the following

* Oracle REST Data Services has been installed and configured on the following server, port, and context path: `localhost:8080/ords/`
* Oracle REST Data Services is running in standalone mode
* Oracle REST Data Services installation was performed using a database *Basic Connection* type with the following attributes:

  * Server: `localhost`
  * Port: `1521`
  * Service name:`ORCLPDB1`

>IMPORTANT: The examples in this tutorial assume that Oracle REST Data Services has been installed and configured in a single instance database *or* Pluggable Database (PDB). The examples and images in this guide will refer to the PDB as `ORCLPDB1`.

### Available client applications for this tutorial

The examples in this tutorial can be completed with the choice of your client application:

* SQLcl
* Oracle Database Actions
* Oracle SQL Developer
* Additionally, certain sections of this tutorial will require the use of a web browser.

> NOTE: For a complete list of currently supported web browsers, please refer [here](https://www.oracle.com/middleware/technologies/browser-policy.html).

<!-- #### Oracle SQL Developer

If you are completing this tutorial using Oracle SQL Developer desktop application (_aka_ client), topics covered will include:

1. REST-Enable a Database Table
2. Creating a RESTful Service through the Connections Navigator
3. Creating a RESTful Service from a SQL Query
4. Protect Resources
5. Register an OAuth Client Application

#### Oracle SQLcl

If you are completing this tutorial using the Oracle SQLcl command line application, topics covered with include:

1.
2.
3.
4.
5.
6.

## Using Oracle SQL Developer 

### .....

## Using SQLcl -->

### Getting Started with Oracle RESTful Services

This section will guide you through the following steps:

* Creating a new database user with required roles and privileges for RESTful access
* Creating a new database table
* Inserting data into the newly-created database table
* Creating a *Resource* by auto-REST-enabling the newly-created database table
* Accessing this new Resource via `localhost`

  > NOTE: We recommend you follow the steps in this tutorial as closely as possible, including using the specified names for schemas and database objects. Once you have completed the tutorial as prescribed, feel free to try it again using alternate schema and database object names.

### Create a new user and REST-enable their schema

1. Using SQLcl, connect to your database as the `SYS` user.

   ![Logging in with SQLcl as the `SYS` user](../ordsQuickStartGuideImages/sql-cl-login-as-sys.png)
   *Logging in with SQLcl as the `SYS` user*

2. Next, create a new `ORDSTEST` user with the following Privileges, Roles, and Tablespace Quota:

   ```sql
   CREATE USER ORDSTEST IDENTIFIED BY <password>;
   GRANT "CONNECT" TO ORDSTEST;
   GRANT "RESOURCE" TO ORDSTEST;
   GRANT UNLIMITED TABLESPACE TO ORDSTEST;
   ```

   ![Create the ORDSTEST user with role, privilege, and tablespace quota](../ordsQuickStartGuideImages/ordstest-user-roles-privileges-tablespace-quota.png)
   *Creating the ORDSTEST user with role, privilege, and tablespace quota*

3. Next, execute the `ORDS_ADMIN.ENABLE_SCHEMA` PL/SQL Procedure. This procedure grants the 'ORDSTEST' user REST access.

   ```pl/sql
   BEGIN
    ORDS_ADMIN.ENABLE_SCHEMA(
        P_ENABLED => TRUE,
        P_SCHEMA => 'ORDSTEST',
        P_URL_MAPPING_TYPE => 'BASE_PATH',
        P_URL_MAPPING_PATTERN => 'ordstest',
        P_AUTO_REST_AUTH => FALSE
    );
    COMMIT;
   END;
   ```

   ![Executing the ORDS.ENABLE_SCHEMA PL/SQL Procedure](../ordsQuickStartGuideImages/ords-enable-ordstest-schema-pl-sql-proc.png)
   *Executing the ORDS.ENABLE_SCHEMA PL/SQL Procedure*

> NOTE: The P_URL_MAPPING_PATTERN parameter *must be* lowercase.

> NOTE: Notice how the `P_AUTO_REST_AUTH` parameter is set to `FALSE`. Setting this parameter to FALSE allows any user access to the ORDS metadata catalogue without the need for user authentication.

> TIP: Additional information on the ORDS PL/SQL Package can be found in [this section](https://docs.oracle.com/en/database/oracle/oracle-rest-data-services/23.1/orddg/ORDS-reference.html#GUID-E4476C14-01B1-4EA4-94D3-73B92C8C9AB3) of the Oracle REST Data Services Developer's Guide.

### Connect as the new user and auto-REST-enable a table

Now that the `ORDSTEST` user schema has been REST-enabled. You may access Database Actions, as the `ORDSTEST` user.

1. Navigate to this URL: `http://localhost:8080/ords/sql-developer`

   ![Navigating to the Database Actions Launchpad](../ordsQuickStartGuideImages/log-in-database-actions-as-ordstest.png)
*Navigating to SQL Developer Web*

2. Next, sign in as the `ORDSTEST` user with the username `ORDSTEST` and Password `oracle` (your password may differ). And click the `Sign in` button.

   Once the page loads, you will see the Database Actions Launchpad, as well as the various categories available to the `ORDSTEST` user.

   ![The Database Actions Launchpad](../ordsQuickStartGuideImages/database-actions-launchpad-as-ordstest-user.png)
   *The Database Actions Launchpad*

<!-- - You may sign out of Database Actions and continue to the next section of this tutorial.  -->

### Connect as the new user and auto REST-enable a table

> IMPORTANT: The following tasks will be completed as the `ORDSTEST` user.

<!-- 1. Log out as SYS and using SQLcl reconnect as the `ORDSTEST` user. The tutorial uses the following connection string: `+sql ordstest/oracle@localhost:1521/ORCLPDB1+`
+
.Connecting to ORCLPDB1 as the `ORDSTEST` user.
image::connect-as-ordstest-with-sqlcl.png[]  -->
1. From the Database Actions Launchpad, select SQL, under the Development category of the dashboard.

    ![selecting-the-sql-worksheet-as-ordstest-user](../ordsQuickStartGuideImages/selecting-the-sql-worksheet-as-ordstest-user.png)
    *Navigating to the SQL Worksheet*

2. Once the SQL Worksheet loads, use the SQL below to create the `EMP` table.

   ```sql
   CREATE TABLE EMP (
       EMPNO NUMBER(4,0),
       ENAME VARCHAR2(10 BYTE),
       JOB VARCHAR2(9 BYTE),
       MGR NUMBER(4,0),
       HIREDATE DATE,
       SAL NUMBER(7,2),
       COMM NUMBER(7,2),
       DEPTNO NUMBER(2,0),
       CONSTRAINT PK_EMP PRIMARY KEY (EMPNO)
       );
   ```

3. With the `EMP` table successfully created, insert the following sample data:

    ```sql
    Insert into EMP (EMPNO,ENAME,JOB,MGR,HIREDATE,SAL,COMM,DEPTNO) values
    (7369,'SMITH','CLERK',7902,to_date('17-DEC-80','DD-MON-RR'),800,null,20);
    Insert into EMP (EMPNO,ENAME,JOB,MGR,HIREDATE,SAL,COMM,DEPTNO) values
    (7499,'ALLEN','SALESMAN',7698,to_date('20-FEB-81','DD-MON-RR'),1600,300,30);
    Insert into EMP (EMPNO,ENAME,JOB,MGR,HIREDATE,SAL,COMM,DEPTNO) values
    (7521,'WARD','SALESMAN',7698,to_date('22-FEB-81','DD-MON-RR'),1250,500,30);
    Insert into EMP (EMPNO,ENAME,JOB,MGR,HIREDATE,SAL,COMM,DEPTNO) values
    (7566,'JONES','MANAGER',7839,to_date('02-APR-81','DD-MON-RR'),2975,null,20);
    Insert into EMP (EMPNO,ENAME,JOB,MGR,HIREDATE,SAL,COMM,DEPTNO) values
    (7654,'MARTIN','SALESMAN',7698,to_date('28-SEP-81','DD-MON-RR'),1250,1400,30); 
    Insert into EMP (EMPNO,ENAME,JOB,MGR,HIREDATE,SAL,COMM,DEPTNO) values
    (7698,'BLAKE','MANAGER',7839,to_date('01-MAY-81','DD-MON-RR'),2850,null,30);
    Insert into EMP (EMPNO,ENAME,JOB,MGR,HIREDATE,SAL,COMM,DEPTNO) values
    (7782,'CLARK','MANAGER',7839,to_date('09-JUN-81','DD-MON-RR'),2450,null,10);
    Insert into EMP (EMPNO,ENAME,JOB,MGR,HIREDATE,SAL,COMM,DEPTNO) values
    (7788,'SCOTT','ANALYST',7566,to_date('19-APR-87','DD-MON-RR'),3000,null,20);
    Insert into EMP (EMPNO,ENAME,JOB,MGR,HIREDATE,SAL,COMM,DEPTNO) values
    (7839,'KING','PRESIDENT',null,to_date('17-NOV-81','DD-MON-RR'),5000,null,10);
    Insert into EMP (EMPNO,ENAME,JOB,MGR,HIREDATE,SAL,COMM,DEPTNO) values
    (7844,'TURNER','SALESMAN',7698,to_date('08-SEP-81','DD-MON-RR'),1500,0,30);
    Insert into EMP (EMPNO,ENAME,JOB,MGR,HIREDATE,SAL,COMM,DEPTNO) values
    (7876,'ADAMS','CLERK',7788,to_date('23-MAY-87','DD-MON-RR'),1100,null,20);
    Insert into EMP (EMPNO,ENAME,JOB,MGR,HIREDATE,SAL,COMM,DEPTNO) values
    (7900,'JAMES','CLERK',7698,to_date('03-DEC-81','DD-MON-RR'),950,null,30);
    Insert into EMP (EMPNO,ENAME,JOB,MGR,HIREDATE,SAL,COMM,DEPTNO) values
    (7902,'FORD','ANALYST',7566,to_date('03-DEC-81','DD-MON-RR'),3000,null,20);
    Insert into EMP (EMPNO,ENAME,JOB,MGR,HIREDATE,SAL,COMM,DEPTNO) values
    (7934,'MILLER','CLERK',7782,to_date('23-JAN-82','DD-MON-RR'),1300,null,10);
    commit;
    ```

   ![inserting-emp-data-into-sql-worksheet-as-ordstest-user](../ordsQuickStartGuideImages/inserting-emp-data-into-sql-worksheet-as-ordstest-user.png)
   *Inserting data into the `EMP` table*

4. With the `EMP` table created and populated with data, you will now auto-REST enable it. From the Navigator Panel, right mouse-click on the table name, navigate to `REST`, then click `Enable`.

   ![selecting-rest-enable-from-navigator-panel](../ordsQuickStartGuideImages/selecting-rest-enable-from-navigator-panel.png)
   *Using the Navigator Panel to select `REST` > `Enable`*

   A `REST Enable Object` slider will appear. After inspecting the parameters that have automatically been generated for you, click the `Enable` button located at the bottom of the slider.

   ![inspecting-parameters-of-emp-auto-rest-slider](../ordsQuickStartGuideImages/inspecting-parameters-of-emp-auto-rest-slider.png)
   *Reviewing the `REST Enable Object` Slider*`

   A message slider will appear, confirming that the `EMP` table has been REST-enabled.

   ![ords-confirming-successful-auto-rest-of-emp-table](../ordsQuickStartGuideImages/ords-confirming-successful-auto-rest-of-emp-table.png)
   *Confirmation that the `EMP` table has been REST-enabled*

   <!-- > NOTE: Alternatively, t  For this   n a previous step the `+SYS+` user enabled the `+ORDSTEST+` _schema_. However in this step the `+ORDSTEST+` user will now REST-enable the `+EMP+` with the following PL/SQL Procedure:  -->

### Testing the auto REST-enabled endpoint

1. You can quickly identify database objects that have been auto-REST enabled by looking for the plug icon next to it's name.

   ![plug-icon-indicating-auto-rest-enabled-table](../ordsQuickStartGuideImages/plug-icon-indicating-auto-rest-enabled-table.png)
   *Plug icon indicating a database object has been auto-REST enabled*

   > NOTE: Click you may need to click the `Refresh` button in the Navigator Panel to display this icon.

   ![click-refresh-in-the-navigator-panel](../ordsQuickStartGuideImages/click-refresh-in-the-navigator-panel.png)
   *Clicking the `Refresh` button to display database objects*

2. You can review and retrieve the REST endpoints for the `EMP` table by right-clicking on the object's name then `REST` then `cURL command`.

   ![locating-curl-command-to-test-rest-endpoint](../ordsQuickStartGuideImages/locating-curl-command-to-test-rest-endpoint.png)
   *Navigating to the `cURL command` menu item*

3. A slider will appear. You'll notice the various HTTP Methods available to an auto-REST enabled resource.

    * `GET ALL`
    * `GET` Single
    * `POST`
    * `BATCH LOAD`
    * `PUT`
    * `DELETE`

   Copy the URL portion of the `GET ALL` cURL command.

   ![copying-get-all-uri-for-emp-table](../ordsQuickStartGuideImages/copying-get-all-uri-for-emp-table.png)
   *Copying the `GET ALL` URL from the `cURL command`*

4. Open a new browser tab, paste the URL into the Address Bar, and press Enter on your keyboard.

   ![results-testing-emp-uri-in-browser](../ordsQuickStartGuideImages/results-testing-emp-uri-in-browser.png)
   *Reviewing the results of the `GET ALL` URI in the browser*

5. You will notice a list of the first 25 items in the `EMP` table. Collapsing the `items` array, will reveal other helpful links, automatically included with all auto-REST enabled resources.

   ![collapsing-items-to-reveal-provided-links](../ordsQuickStartGuideImages/collapsing-items-to-reveal-provided-links.png)
   *Collapsing `items` to reveal additional, helpful links*

   > NOTE: ORDS automatically sets pagination to 25 results, although this setting can be changed later if required. This configuration falls outside the scope of this Quick Start Guide.

<!-- [source,PL/SQL,indent=0]
----
BEGIN
    ORDS.ENABLE_OBJECT(
        P_ENABLED => TRUE,
        P_SCHEMA => 'ORDSTEST',
        P_OBJECT => 'EMP',
        P_OBJECT_TYPE => 'TABLE',
        P_OBJECT_ALIAS => 'emp',
        P_AUTO_REST_AUTH => FALSE
    );
    COMMIT;
END;
----
+
.REST-enable the `+EMP+` table.
image::ords-enable-object-pl-sql-procedure.png[]
+
IMPORTANT: Notice how the `+P_OBJECT_ALIAS+` parameter in this example is lowercase. This is because the alias will soon be appended to the Base URI, like this: `+http://
localhost:8080/ords/ordstest/emp/+`. Character casing is important, and lowercase required.
+

NOTE: Executing this PL/SQL Procedure also _automatically_ enables `+GET+`,`+PUT+`,`+POST+`,`+DELETE+` methods, as well as the creation of metadata-catalog endpoints.

5. The `+EMP+` table is now exposed as an _auto_ REST-enabled HTTP endpoint. To test this endpoint, open a web browser and navigate to the following URL: `+http://
localhost:8080/ords/ordstest/emp/+`.
+
.Reviewing the `+GET+` endpoint.
image::reviewing-emp-get-endpoint-in-browser.png[]
+
- Notice how the `+ORDSTEST+` schema has been exposed at the `+/ordstest+` path and the `+EMP+` table has been exposed at the `+/emp/+` path.
- If you were to scroll to the bottom of this page, you'll see that ORDS has provided additional links for reference. btn:[Click] the `+metadata-catalog+` link: `+http://localhost:80808/ords/ordstest/metadata-catalog/emp+`
+
.Reviewing additional links provided by ORDS.
image::reviewing-emp-links-from-get-endpoint.png[]
+
- If you've worked with the OpenAPI Specification, then these fileds may look familiar. Oracle REST Data Services conforms to the OpenAPI Specification. In particular, you'll see the OpenAPI object fields described in this endpoint. 
+
TIP: More information on the OpenAPI Specification can be found https://swagger.io/specification/[here]. 
+

.Reviewing the `+EMP+` metadata catalog.
image::viewing-emp-ords-metadata.png[]

=== Creating custom Oracle REST APIs using ORDS-packaged PL/SQL procedures 

ORDS installation will include the addition of a PL/SQL Package. In it contains many PL/SQL procedures and functions used for developing RESTful services for your Oracle database. In this secion you will learn how to create a basic custom Oracle REST API. The PL/SQL procedures used are: 

- `+ORDS.DEFINE_MODULE+`
- `+ORDS.DEFINE_TEMPLATE+`
- `+ORDS.DEFINE_HANDLER+`

1. First, we'll define a simple Resource Module using the `+ORDS.DEFINE_MODULE+` procedure. For this example, most of the default parameter will remain unmodified. However,`+P_MODULE_NAME+` and `+P_BASE_PATH+` parameters will be changed for this tutorial:
+
[source,PL/SQL,indent=0]
----
BEGIN
    ORDS.DEFINE_MODULE(
        p_module_name => 'Demo',
        p_base_path => '/demo/'
    );
END;
----
+

2. Next, you'll define a Resource Template for the `+my.tickets+` Resource Module. In this example, you will retain many of the default parameters, with the exception of the Resource Module name and Template Pattern parameters:
+
[source,PL/SQL,indent=0]
----
BEGIN
  ORDS.DEFINE_TEMPLATE(
    p_module_name => 'Demo',
    p_pattern => 'emp/'
  );
END;
----
+

3. Finally, you'll define the Handler parameters for this Resource Template (and by association the Resource Module as well). Unlike the previous steps, many of the default parameters will be slightly modified: 
+
[source,PL/SQL,indent=0]
----
BEGIN
  ORDS.DEFINE_HANDLER(
    p_module_name => 'my.tickets',
    p_pattern => '.',
    p_method  => 'POST',
    p_mimes_allowed => 'application/json',
    p_source_type => ords.source_type_plsql,
    p_source => '
      declare
        l_owner varchar2(255);
        l_payload blob;
        l_id number;
      begin
        l_payload := :body;
        l_owner := :owner;
        if ( l_owner is null ) then
          l_owner := :current_user;
        end if;
        l_id := ticket_api.create_ticket(
          p_json_entity => l_payload,
          p_author => l_owner
        );
        :location := ''./'' || l_id;
        :status := 201;
      end;
      '
  );
END;
----
+
+
[source,PL/SQL,indent=0]
----
----
+
+
[source,PL/SQL,indent=0]
----
----
+ -->
