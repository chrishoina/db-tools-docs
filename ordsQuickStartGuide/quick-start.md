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

  > **NOTE:** The latest version of SQLcl can be obtained [here](https://www.oracle.com/database/sqldeveloper/technologies/sqlcl/download/) *or* through Homebrew with the following `brew install --cask sqlcl` command. Additional SQLcl installation information can be found on [Homebrew](https://formulae.brew.sh/cask/sqlcl#default).

  > **NOTE:** The latest version of Oracle SQL Developer can be obtained [here](https://www.oracle.com/database/sqldeveloper/technologies/download/).

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

  > **IMPORTANT:** The examples in this tutorial assume that Oracle REST Data Services has been installed and configured in a single instance database *or* Pluggable Database (PDB). The examples and images in this guide will refer to the PDB as `ORCLPDB1`.

### Available client applications for this tutorial

The examples in this tutorial can be completed with the choice of your client application:

* SQLcl
* Oracle Database Actions
* Oracle SQL Developer
* Additionally, certain sections of this tutorial will require the use of a web browser.

  > **NOTE:** For a complete list of currently supported web browsers, please refer [here](https://www.oracle.com/middleware/technologies/browser-policy.html).

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

  > **NOTE:** We recommend you follow the steps in this tutorial as closely as possible, including using the specified names for schemas and database objects. Once you have completed the tutorial as prescribed, feel free to try it again using alternate schema and database object names.

#### Create a new user and REST-enable their schema <a id="create-a-new-user"></a>

1. Using SQLcl, connect to your database as the `SYS` user.

   ![Logging in with SQLcl as the `SYS` user](./ordsQuickStartGuideImages/sql-cl-login-as-sys.png)
   *Logging in with SQLcl as the `SYS` user*

2. Next, create a new `ORDSTEST` user with the following Privileges, Roles, and Tablespace Quota:

   ```sql
   <copy>
   CREATE USER ORDSTEST IDENTIFIED BY <password>;
   GRANT "CONNECT" TO ORDSTEST;
   GRANT "RESOURCE" TO ORDSTEST;
   GRANT UNLIMITED TABLESPACE TO ORDSTEST;
   </copy>
   ```

   ![Create the ORDSTEST user with role, privilege, and tablespace quota](./ordsQuickStartGuideImages/ordstest-user-roles-privileges-tablespace-quota.png)
   *Creating the ORDSTEST user with role, privilege, and tablespace quota*

3. Next, connect to your database as the `ORDSTEST` user and execute the `ORDS.ENABLE_SCHEMA;` PL/SQL Procedure. This procedure grants the `ORDSTEST` user REST access.

   ```pl/sa;
   <copy>
   EXECUTE ORDS.ENABLE_SCHEMA;
   </copy>
   ```


<!-- 3. Next, execute the `ORDS_ADMIN.ENABLE_SCHEMA` PL/SQL Procedure. This procedure grants the `ORDSTEST` user REST access.

   ```pl/sql
   <copy>
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
   </copy>
   ``` -->

   ![Executing the ORDS.ENABLE_SCHEMA PL/SQL Procedure](./ordsQuickStartGuideImages/execute-ords-enable-schema-procedure-as-ordstest-user.png)
   *Executing the ORDS.ENABLE_SCHEMA PL/SQL Procedure*

   <!-- > **NOTE:** The P_URL_MAPPING_PATTERN parameter *must be* lowercase.

   > **NOTE:** Notice how the `P_AUTO_REST_AUTH` parameter is set to `FALSE`. Setting this parameter to FALSE allows any user access to the ORDS metadata catalogue without the need for user authentication. -->

   > **TIP:** Additional information on the ORDS PL/SQL Package can be found in [this section](https://docs.oracle.com/en/database/oracle/oracle-rest-data-services/23.1/orddg/ORDS-reference.html#GUID-E4476C14-01B1-4EA4-94D3-73B92C8C9AB3) of the Oracle REST Data Services Developer's Guide.

#### Connect as the new user and auto-REST-enable a table

Now that the `ORDSTEST` user schema has been REST-enabled. You may access Database Actions, as the `ORDSTEST` user.

1. Navigate to this URL: `http://localhost:8080/ords/sql-developer`

   ![Navigating to the Database Actions Launchpad](./ordsQuickStartGuideImages/log-in-database-actions-as-ordstest.png)
   *Navigating to SQL Developer Web*

2. Next, sign in as the `ORDSTEST` user with the username `ORDSTEST` and Password `oracle` (your password may differ). And click the `Sign in` button.

   Once the page loads, you will see the Database Actions Launchpad, as well as the various categories available to the `ORDSTEST` user.

   ![The Database Actions Launchpad](./ordsQuickStartGuideImages/database-actions-launchpad-as-ordstest-user.png)
   *The Database Actions Launchpad*

<!-- - You may sign out of Database Actions and continue to the next section of this tutorial.  -->

#### Connect as the new user and auto REST-enable a table

  > **IMPORTANT:** The following tasks will be completed as the `ORDSTEST` user.

<!-- 1. Log out as SYS and using SQLcl reconnect as the `ORDSTEST` user. The tutorial uses the following connection string: `+sql ordstest/oracle@localhost:1521/ORCLPDB1+`
+
.Connecting to ORCLPDB1 as the `ORDSTEST` user.
image::connect-as-ordstest-with-sqlcl.png[]  -->
1. From the Database Actions Launchpad, select SQL, under the Development category of the dashboard.

    ![selecting-the-sql-worksheet-as-ordstest-user](./ordsQuickStartGuideImages/selecting-the-sql-worksheet-as-ordstest-user.png)
    *Navigating to the SQL Worksheet*

2. Once the SQL Worksheet loads, use the SQL below to create the `EMP` table.

   ```sql
   <copy>
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
   </copy>
   ```

3. With the `EMP` table successfully created, insert the following sample data:

    ```sql
    <copy>
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
    </copy>
    ```

   ![inserting-emp-data-into-sql-worksheet-as-ordstest-user](./ordsQuickStartGuideImages/inserting-emp-data-into-sql-worksheet-as-ordstest-user.png)
   *Inserting data into the `EMP` table*

4. With the `EMP` table created and populated with data, you will now auto-REST enable it. From the Navigator Panel, right mouse-click on the table name, navigate to `REST`, then click `Enable`.

   ![selecting-rest-enable-from-navigator-panel](./ordsQuickStartGuideImages/selecting-rest-enable-from-navigator-panel.png)
   *Using the Navigator Panel to select `REST` > `Enable`*

   A `REST Enable Object` slider will appear. After inspecting the parameters that have automatically been generated for you, click the `Enable` button located at the bottom of the slider.

   ![inspecting-parameters-of-emp-auto-rest-slider](./ordsQuickStartGuideImages/inspecting-parameters-of-emp-auto-rest-slider.png)
   *Reviewing the `REST Enable Object` Slider*`

   A message slider will appear, confirming that the `EMP` table has been REST-enabled.

   ![ords-confirming-successful-auto-rest-of-emp-table](./ordsQuickStartGuideImages/ords-confirming-successful-auto-rest-of-emp-table.png)
   *Confirmation that the `EMP` table has been REST-enabled*

   <!-- > NOTE: Alternatively, t  For this   n a previous step the `+SYS+` user enabled the `+ORDSTEST+` _schema_. However in this step the `+ORDSTEST+` user will now REST-enable the `+EMP+` with the following PL/SQL Procedure:  -->

#### Testing the auto REST-enabled endpoint

1. You can quickly identify database objects that have been auto-REST enabled by looking for the plug icon next to it's name.

   ![plug-icon-indicating-auto-rest-enabled-table](./ordsQuickStartGuideImages/plug-icon-indicating-auto-rest-enabled-table.png)
   *Plug icon indicating a database object has been auto-REST enabled*

   > **NOTE:** Click you may need to click the `Refresh` button in the Navigator Panel to display this icon.

   ![click-refresh-in-the-navigator-panel](./ordsQuickStartGuideImages/click-refresh-in-the-navigator-panel.png)
   *Clicking the `Refresh` button to display database objects*

2. You can review and retrieve the REST endpoints for the `EMP` table by right-clicking on the object's name then `REST` then `cURL command`.

   ![locating-curl-command-to-test-rest-endpoint](./ordsQuickStartGuideImages/locating-curl-command-to-test-rest-endpoint.png)
   *Navigating to the `cURL command` menu item*

3. A slider will appear. You'll notice the various HTTP Methods available to an auto-REST enabled resource.

    * `GET ALL`
    * `GET` Single
    * `POST`
    * `BATCH LOAD`
    * `PUT`
    * `DELETE`

   Copy the URL portion of the `GET ALL` cURL command.

   ![copying-get-all-uri-for-emp-table](./ordsQuickStartGuideImages/copying-get-all-uri-for-emp-table.png)
   *Copying the `GET ALL` URL from the `cURL command`*

4. Open a new browser tab, paste the URL into the Address Bar, and press Enter on your keyboard.

   ![results-testing-emp-uri-in-browser](./ordsQuickStartGuideImages/results-testing-emp-uri-in-browser.png)
   *Reviewing the results of the `GET ALL` URI in the browser*

5. You will notice a list of the first 25 items in the `EMP` table. Collapsing the `items` array, will reveal other helpful links, automatically included with all auto-REST enabled resources.

   ![collapsing-items-to-reveal-provided-links](./ordsQuickStartGuideImages/collapsing-items-to-reveal-provided-links.png)
   *Collapsing `items` to reveal additional, helpful links*

   > NOTE: ORDS automatically sets pagination to 25 results, although this setting can be changed later if required. This configuration falls outside the scope of this Quick Start Guide.

### Creating a RESTful Service through the REST Workshop

This section explains how to create a RESTful service using REST Workshop in Database Actions. The REST Workshop enables you to create and edit RESTful service definitions.

#### Navigating to the REST Workshop

To create and test a RESTful service in the REST Workshop, follow these steps:

1. While logged in as the `ORDSTEST` user, navigate to the Database Actions Launchpad. From there select the `REST`card, located in the Development category.

   ![navigating-to-rest-workshop-from-launchpad](./ordsQuickStartGuideImages/navigating-to-rest-workshop-from-launchpad.png )
   *Selecting the `REST` card from the Launchpad*

2. Once the REST Workshop screen loads, click the `Modules` widget. A `Modules` dashboard will load. Next, click the `+ Create Module` button, located in the upper right-hand corner of the dashboard.

     ![locating-the-modules-card-in-rest-workshop](./ordsQuickStartGuideImages/locating-the-modules-card-in-rest-workshop.png)
     *Locating the Modules widget*

     ![create-new-module-in-module-dashboard](./ordsQuickStartGuideImages/create-new-module-in-module-dashboard.png)
     *Selecting the `+ Create Module` button*

3. A **Create Module** slider will appear. Enter in the following information:

   * **Module Name**: Any desired name for the connection. For example, `demo.module`
   * **URI Prefix**: `/demo/`
   * **Pagination Size**: `25`

     ![adding-values-to-module-fields](./ordsQuickStartGuideImages/adding-values-to-module-fields.png)
     *Adding values to the Module fields*

   * In the **Protected by Privilege** field select `Not Protected`.

     ![selecting-not-protected-to-module](./ordsQuickStartGuideImages/selecting-not-protected-to-module.png)
     *Publishing the Module without requiring a Privilege*

4. Click `Create`, your Module settings will be saved, and you'll be taken to the Resource Templates page. Click the `+ Create Template` button.

   ![create-template-screen](./ordsQuickStartGuideImages/create-template-screen.png)
   *Confirmation notification for Module creation*

   ![clicking-create-template-button](./ordsQuickStartGuideImages/clicking-create-template-button.png)
   *Clicking the `Create Template` button*

5. A **Create Template** slider will appear. In the `URI Template` field, enter: `emp/`. For this demonstration, you'll retain the detault settings. Click the `Create` button.

   ![create-template-slider](./ordsQuickStartGuideImages/create-template-slider.png)
   *Entering in the URI `Template`*

6. You'll be automatically taken to the **Create Handler** page. For this tutorial, you will create a `GET` method. Click the `+ Create Handler` button.

   ![clicking-create-handler-button](./ordsQuickStartGuideImages/clicking-create-handler-button.png)
   *Clicking the `Create Handler` button*

7. A **Create Handler** slider will appear. Verify the following settings:

   * **Method**: `GET`
   * **Items Per Page**: `7`
   * **Source Type**: `Collection Query`

     ![entering-initial-fields-in-handler-slider](./ordsQuickStartGuideImages/entering-initial-fields-in-handler-slider.png)
     *Verifying fields of the Resource Handler*

8. In the **Source** field, place the following SQL query:

   ```sql
   <copy>
   SELECT
     INITCAP(ENAME) name,
     lower(job) job,
     TO_CHAR(sal,'9G999','NLS_NUMERIC_CHARACTERS=",."') salary,
     hiredate
   FROM
   emp
   </copy> 
   ```
  
   ![adding-sql-query-to-handler-field](./ordsQuickStartGuideImages/adding-sql-query-to-handler-field.png)
   *`SQL` query added to the Source field*

9. Click the **Create** button. You'll be taken to the Resource Handler page.

   ![handler-successfully-created](./ordsQuickStartGuideImages/handler-successfully-created.png)
   *Confirmation that Resource Handler was created*

10. To test the SQL query you may click the `Play` icon. The results of the query will appear in the output window below.

    ![clicking-play-button-for-query-results](./ordsQuickStartGuideImages/clicking-play-button-for-query-results.png)
    *Reviewing results of the Handler `SQL` query*

11. To test the RESTful service, click the `Open in a new tab` icon. A new browser tab will appear, with the results from the `GET` method.

    ![open-in-new-tab-icon-to-test-endpoint](./ordsQuickStartGuideImages/open-in-new-tab-icon-to-test-endpoint.png)
    *Opening the URI in a new browser tab*

    ![reviewing-results-in-separate-broweser-tab](./ordsQuickStartGuideImages/reviewing-results-in-separate-broweser-tab.png)
    *Reviewing the `JSON` response in the browser window*

#### Creating a Privilege using Database Actions

Controlling access to protected resources is done by defining privileges. Privileges restrict access to only users having at least one of a set of specified roles. A privilege is then associated with one or more resource modules: before those resource modules can be accessed, the user must be authenticated and then authorized to ensure that the user has one of the required roles.  

1. To protect a resource, begin by creating a Privilege. Navigate to the `REST` Workshop.

2. Under the Security menu item, click on Privileges.

   ![clicking-create-privileges-menu-option](./ordsQuickStartGuideImages/navigating-to-privileges-menu-option.png)
   *Selecting `Privileges` under Security*

3. Then, click the `+ Create Privilege` button. A `Create Privilege` slider will appear.

   ![clicking-create-privileges-button](./ordsQuickStartGuideImages/clicking-the-create-privileges-button.png)

   ![privileges-slider-appears](./ordsQuickStartGuideImages/privileges-slider-appears.png)

4. Enter the following for the field values:

   * `Label:` Demo module privilege
   * `Name:` demo.module.privilege
   * `Description:` A Privilege created for demonstrating privileges for the `demo.module` Resource Module.

     ![privileges-definition-fields](./ordsQuickStartGuideImages/creating-privilege-definition-for-module.png)

5. Next, navigate to the **Protected Modules** table. Move the `demo.module` Resource Module from the left column to the right column. This ensures that the `demo.module` Resource Module is associated with this Privilege.

   ![demo-module-available-column](./ordsQuickStartGuideImages/demo-module-available-column.png)

   ![demo-module-selected-column](./ordsQuickStartGuideImages/demo-module-selected-column.png)

6. Once complete, click `Create`. You will see a confirmation message appear, indicating the successful creation of a new Privilege. You should also see the newly created Privilege in your Privileges dashboard.

   ![privilege-creation-confirmation](./ordsQuickStartGuideImages/privilege-creation-confirmation.png)

7. To test this Privilege, navigate to the `Path` of the `demo.module` and copy the `emp/` URI.

   ![navigate-to-demo-module-to-test-privilege](./ordsQuickStartGuideImages/navigate-to-demo-module-to-test-privilege.png)

   ![navigate-to-path-to-copy-uri-to-test-privilege](./ordsQuickStartGuideImages/navigate-to-path-to-copy-uri-to-test-privilege.png)

8. Next, `Sign Out` of Database actions. Open a new browser window. Paste the URI in the address bar and click `Return / Enter`.

   ![sign-out-of-database-actions-to-test-privilege](./ordsQuickStartGuideImages/sign-out-of-database-actions-to-test-privilege.png)

9. You'll receive a `401 Unauthorized` error, with a message indicating that the resource is now protected. Notice that a `Sign In` prompt appears. Since this Privilege has not been associated with a specific role, any user that has been granted the `Connect` role may sign-in to view the response from this request. Sign-in with your database credentials to view the resource.

   ![navigating-to-path-forces-sign-in-to-view-emp-path](./ordsQuickStartGuideImages/navigating-to-path-forces-sign-in-to-view-emp-path.png)

   ![sign-in-with-credentials-to-test-path-privilege](./ordsQuickStartGuideImages/sign-in-with-credentials-to-test-path-privilege.png)

10. The contents of the JSON document should now be visible.

   ![after-sign-in-emp-path-visible-testing-privilege](./ordsQuickStartGuideImages/after-sign-in-emp-path-visible-testing-privilege.png)

### Register an OAuth Client Application

This topic explains how to register your applications (called "third-party" applications here) to access a REST API.

OAuth 2.0 is a standard Internet protocol that provides a means for HTTP servers providing REST APIs to give limited access to third party applications on behalf of an end user.

OAuth 2.0 protocol provides a means for HTTP servers, like those that provide access to REST APIs, to give limited access of these REST APIs to third party applications on behalf of an authenticated end user.

Before a third party application can access a REST API, it must:

   1. be registered, *and*
   2. the user must approve access

And before the application can be registered, it must be assigned a user identity that enables the user to register applications. Users possessing the SQL Developer role (such as the user you created in [Chapter 1](#create-a-new-user)) of this guide are permitted to register OAuth 2.0 clients.

  > **TIP:** In a real application, you may want to provision specific users that can register OAuth clients; these users should be granted the OAuth Client Developer role.

  > **NOTE:** The following example is not intended to serve as a full-featured demonstration for creation and integration for a third party application. The example simply outlines the core concepts of the OAuth 2.0 protocol.

1. From the REST Workshop dashboard, locate the `OAuth Clients` menu option from the `Security` tab. Select this option to be taken to the `OAuth Clients` dashboard.

   ![navigate-to-oauth-clients-menu-option](./ordsQuickStartGuideImages/navigate-to-oauth-clients-menu-option.png)

2. From the OAuth Client dashboard, click the `+ Create OAuth Client` button. A `Create OAuth Client` slider will appear.

      ![click-create-oauth-client](./ordsQuickStartGuideImages/click-create-oauth-client.png)

3. Ensure `CLIENT_CRED` has been selected for `Grant Type`.

   ![ensure-client-credentials-has-been-selected](./ordsQuickStartGuideImages/ensure-client-credentials-has-been-selected.png)

4. Next, enter in the following to the empty slider fields:

   * `Name:` example_oauth_client
   * `Description:` An example OAuth 2.0 client using the Client Credentials grant type.
   * `Support URI`: https://example.com  
   * `Support Email:` email@example.com

     ![completing-oauth-slider-fields](./ordsQuickStartGuideImages/completing-oauth-slider-fields.png)

5. After competing the fields, navigate to the `Privileges` tab of the slider. Once there, locate the privilege you created in the previous section. Move it from the Available Privileges column (left) to the Selected Privileges column (right). Then click the `Create` button.

   ![available-privileges-for-oauth-client](./ordsQuickStartGuideImages/available-privileges-for-oauth-client.png)

   ![selected-privileges-for-oauth-client](./ordsQuickStartGuideImages/selected-privileges-for-oauth-client.png)

   > **TIP:** The double arrow moves *all* available privileges to the Selected Privileges column. The single arrow moves *only the currently selected* privileges to the Selected Privileges column.

6. After returning to the OAuth Clients dashboard, you'll notice the newly-created OAuth client.

   ![newly-created-oauth-client-in-dashboard](./ordsQuickStartGuideImages/newly-created-oauth-client-in-dashboard.png)

7. To test the protected resource, navigate to your REST Modules dashboard, and click on your `demo.module`.

   ![navigating-to-demo-module-for-emp-uri](./ordsQuickStartGuideImages/navigating-to-demo-module-for-emp-uri.png)

8. Next, copy the URI for the `emp/` endpoint.

   ![copying-emp-uri-to-clipboard](./ordsQuickStartGuideImages/copying-emp-uri-to-clipboard.png)

9. Open a new terminal session and issue the following curl command:

   ```bash
   <copy>
   curl curl http://localhost:8080/ords/ordstest/demo/emp/
   </copy>
   ```

   > **NOTE:** Your REST endpoint will differ slightly.

10. The response should look something like the following:
  
    ![attempt-get-request-without-access-token-to-protected-emp-uri](./ordsQuickStartGuideImages/attempt-get-request-without-access-token-to-protected-emp-uri.png)

    ```bash
    {
    "code": "Unauthorized"
    "message": "Unauthorized"
    "type": "tag:oracle.com, 2020:error/Unauthorized"
    "instance": "tag:oracle.com, 2020:ecid/KJPTrQ-tIKEPuMU31CoMyQ"
    }
    ```

    This `Unauthorized` message confirms that your REST endpoint has been protected by the privilege created in a previous section.

11. Next, we'll:

    1. authenticate with, *and*
    2. request an Access Token from

    the OAuth 2.0 Authorization Server using the `Client ID` and `Client Secret`of the `example_oauth_client`.

12. From the OAuth Clients dashboard, click on the kebab icon <span>&#8942;</span> found in the `example_oauth_client` card and select `Get Bearer Token`.

    ![get-bearer-token-option-from-kebab-menu](./ordsQuickStartGuideImages/get-bearer-token-option-from-kebab-menu.png)

13. Once the `OAuth Token` modal appears, select the correct shell environment, and copy the curl command to your clipboard.

    ![selecting-correct-shell-for-your-environment](./ordsQuickStartGuideImages/selecting-correct-shell-for-your-environment.png)

    ![copy-bearer-token-curl-command-from](./ordsQuickStartGuideImages/copy-bearer-token-curl-command-from.png)

14. Using the `Client ID` and `Client Secret` provided to you, issue the following curl command to obtain an Access Token:

    ```bash
    curl \
    --user Bx2vfYZkLa9D8_CZXvFL0Q..:xH1nn_CPtitiW5vOUQXrrg.. \
    --data 'grant_type=client_credentials' \
    http://localhost:8080/ords/ordstest/oauth/token
    ```

15. You will receive an Access Token, with expiration.

    ![curl-response-get-access-token](./ordsQuickStartGuideImages/curl-response-get-access-token.png)

    You may now use this Access Token in a subsequent `GET` request to the `emp/` endpoint.

16. You can now access the `emp/` endpoint. Model your curl command as the one below, ensuring you've included the Access Token as a Header in your curl command:

    ```bash
    curl -H "Authorization: Bearer PWMGyNYtzhg9J1r85_oJGQ" http://localhost:8080/ords/ordstest/demo/emp/ | jq
    ```

    ![jq-response-from-get-request](./ordsQuickStartGuideImages/jq-response-from-get-request.png)

    > **NOTE:** You may *optionally* pipe in the `jq` command so the `JSON` response payload is structured in a more readable format.
