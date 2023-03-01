
# Appendix

## 1.2 User Requirements

### ORDS Installer Privileges Script

#### About the script

> Note: This script is used when you do not want to use SYS AS SYSDBA to install, upgrade, repair, and uninstall ORDS for Oracle PDB or Oracle 11g.

A script file is included in each ORDS download package that provides privileges to a user for ORDS:

- install/uninstall
- upgrade
- repair

##### ORDS Installer Privileges script

```sql
Rem  Copyright (c) Oracle Corporation 2014. All Rights Reserved.
Rem
Rem    NAME
Rem      ords_installer_privileges.sql
Rem
Rem    DESCRIPTION
Rem      Provides privileges required to install, upgrade, validate and uninstall 
Rem      ORDS schema, ORDS proxy user and related database objects.
Rem
Rem    NOTES
Rem      This script includes privileges to packages and views that are normally granted PUBLIC 
Rem      because these privileges may be revoked from PUBLIC.
Rem   
Rem
Rem    ARGUMENT:
Rem      1  : ADMINUSER - The database user that will be granted the privilege
Rem
Rem    REQUIREMENTS
Rem      Oracle Database Release 11.1 or later
Rem
Rem    MODIFIED   (MM/DD/YYYY)
Rem      epaglina  09/25/2019  Grant SELECT object privilege if DB version 12.1.0.1.
Rem      epaglina  05/22/2019  Created.
Rem

set define '^'
set serveroutput on
set termout on

define ADMINUSER = '^1'

--
-- System privileges
--
grant alter any table                   to ^ADMINUSER;
grant alter user                        to ^ADMINUSER with admin option;
grant comment any table                 to ^ADMINUSER;
grant create any context                to ^ADMINUSER;
grant create any index                  to ^ADMINUSER;
grant create any job                    to ^ADMINUSER;
grant create any procedure              to ^ADMINUSER;
grant create any sequence               to ^ADMINUSER;
grant create any synonym                to ^ADMINUSER;
grant create any table                  to ^ADMINUSER;
grant create any trigger                to ^ADMINUSER with admin option;
grant create any type                   to ^ADMINUSER;
grant create any view                   to ^ADMINUSER;
grant create job                        to ^ADMINUSER with admin option;
grant create public synonym             to ^ADMINUSER with admin option;
grant create role                       to ^ADMINUSER;
grant create session                    to ^ADMINUSER with admin option;
grant create synonym                    to ^ADMINUSER with admin option;
grant create user                       to ^ADMINUSER;
grant create view                       to ^ADMINUSER with admin option;
grant delete any table                  to ^ADMINUSER;
grant drop any context                  to ^ADMINUSER;
grant drop any role                     to ^ADMINUSER;
grant drop any table                    to ^ADMINUSER;
grant drop any type                     to ^ADMINUSER;
grant drop any synonym                  to ^ADMINUSER;
grant drop public synonym               to ^ADMINUSER with admin option;
grant drop user                         to ^ADMINUSER;
grant execute any procedure             to ^ADMINUSER;
grant execute any type                  to ^ADMINUSER;
grant grant any object privilege        to ^ADMINUSER;
grant insert any table                  to ^ADMINUSER;
grant select any table                  to ^ADMINUSER;
grant update any table                  to ^ADMINUSER;

declare
  c_grant_set_con constant varchar2(255)  := 'grant set container to ' || dbms_assert.enquote_name('^ADMINUSER')
                                           || ' with admin option';
begin
  -- Only for Oracle DB 12c and later
  if sys.dbms_db_version.VERSION >= 12 then
    dbms_output.put_line(c_grant_set_con);
    execute immediate c_grant_set_con;
  end if;
end;
/

--
-- Object privileges with grant option
--
grant execute on sys.dbms_assert        to ^ADMINUSER with grant option;
grant execute on sys.dbms_crypto        to ^ADMINUSER with grant option;
grant execute on sys.dbms_lob           to ^ADMINUSER with grant option;
grant execute on sys.dbms_metadata      to ^ADMINUSER with grant option;
grant execute on sys.dbms_output        to ^ADMINUSER with grant option;
grant execute on sys.dbms_scheduler     to ^ADMINUSER with grant option;
grant execute on sys.dbms_session       to ^ADMINUSER with grant option;
grant execute on sys.dbms_utility       to ^ADMINUSER with grant option;
grant execute on sys.dbms_sql           to ^ADMINUSER with grant option;
grant execute on sys.default_job_class  to ^ADMINUSER with grant option;
grant execute on sys.htp                to ^ADMINUSER with grant option;
grant execute on sys.owa                to ^ADMINUSER with grant option;
grant execute on sys.wpiutl             to ^ADMINUSER with grant option;
grant execute on sys.wpg_docload        to ^ADMINUSER with grant option;

grant select on sys.user_cons_columns   to ^ADMINUSER with grant option;
grant select on sys.user_constraints    to ^ADMINUSER with grant option;
grant select on sys.user_objects        to ^ADMINUSER with grant option;
grant select on sys.user_procedures     to ^ADMINUSER with grant option;
grant select on sys.user_tab_columns    to ^ADMINUSER with grant option;
grant select on sys.user_tables         to ^ADMINUSER with grant option;
grant select on sys.user_views          to ^ADMINUSER with grant option;

--
-- Object privileges
--

-- For Oracle DB 12.1.0.2 and later, grant READ.  Otherwise, grant SELECT.
declare
 type obj_name_list is table of dba_tab_privs.table_name%TYPE;
  list1 obj_name_list := obj_name_list(
                                      'CDB_SERVICES',
                                      'CDB_TABLESPACES',
                                      'DBA_ROLES',
                                      'DBA_SYNONYMS',
                                      'DBA_TABLESPACES',
                                      'DBA_TAB_COLS',
                                      'DBA_TAB_PRIVS',
                                      'DBA_TEMP_FILES',
                                      'PROXY_USERS',
                                      'V_$CONTAINERS',
                                      'V_$DATABASE',
                                      'V_$LISTENER_NETWORK',
                                      'V_$PARAMETER'
                                      );
  -- Include the "with grant option"
  list2 obj_name_list := obj_name_list(
                                      'DBA_OBJECTS',
                                      'DBA_REGISTRY',
                                      'DBA_ROLE_PRIVS',
                                      'DBA_TAB_COLUMNS',
                                      'DBA_USERS',
                                      'SESSION_PRIVS'
                                       );
                                                                           
  c_grant_read constant varchar2(100)  := 'grant read on sys.';
  c_grant_select constant varchar2(100):= 'grant select on sys.';
  c_user_grant constant varchar2(255)  := ' to ' || dbms_assert.enquote_name('^ADMINUSER');
  c_grant_opt constant varchar2(100)   := ' with grant option';
  
  l_use_read boolean          := FALSE;
  l_prod_version varchar2(20) := '';

begin
  if sys.dbms_db_version.VERSION > 12 then
    l_use_read := TRUE;
  elsif sys.dbms_db_version.VERSION = 12 then
    begin
      select version into l_prod_version from sys.v$instance where version like '12.1.0.1.%';
    exception
      when NO_DATA_FOUND then
        -- 12.1.0.2 or later
        l_use_read := TRUE;
      when others then
        null;
    end;
  end if;

  for i in list1.first .. list1.last loop
    if l_use_read then
        -- 12c and later use the READ privilege
      dbms_output.put_line( c_grant_read || list1(i) || c_user_grant);
      execute immediate c_grant_read || list1(i) || c_user_grant;
    elsif (sys.dbms_db_version.VERSION = 12) or
          (sys.dbms_db_version.VERSION = 11 and list1(i) <> 'V_$CONTAINERS') then
      dbms_output.put_line(c_grant_select || list1(i) || c_user_grant);
      execute immediate c_grant_select || list1(i) || c_user_grant;
    end if;
  end loop;
  
  for i in list2.first .. list2.last loop
    if l_use_read then
        -- 12c and later use the READ privilege
      dbms_output.put_line( c_grant_read || list2(i) || c_user_grant || c_grant_opt);
      execute immediate c_grant_read || list2(i) || c_user_grant || c_grant_opt;
    else
      dbms_output.put_line(c_grant_select || list2(i) || c_user_grant || c_grant_opt);
      execute immediate c_grant_select || list2(i) || c_user_grant || c_grant_opt;
    end if;
  end loop;
  
  -- Grant to check if ORDS application is installed in the Application Container
  if (sys.dbms_db_version.version > 12) or (sys.dbms_db_version.version = 12 and sys.dbms_db_version.release > 1) then
    execute immediate c_grant_read || 'DBA_APPLICATIONS' || c_user_grant;
  end if;  
end;
/

-- APEX Support
declare
  c_sel_stmt     constant varchar2(400) := 'select version, schema, status from sys.dba_registry where comp_id = ''APEX''';
  c_grant_select constant varchar2(100) := 'grant select on ';
  c_to_user      constant varchar2(400) := ' to ' || dbms_assert.enquote_name('^ADMINUSER') || ' with grant option';
  l_apex_schema  varchar2(255) := null;
  l_apex_version   varchar2(100) := '';
  l_status         varchar2(100) := null;
  l_tmp_str        varchar2(100) := null;
  l_ver_no         number;
  l_ndx            number;
  
begin
  begin
      execute immediate c_sel_stmt into l_apex_version, l_apex_schema, l_status;
  exception
     when no_data_found then
        null;  -- APEX doesn't exist
  end;
   
  if (l_status is not null) and (l_status = 'VALID') and
      (l_apex_version is not null) and (l_apex_schema is not null) then
   
     l_ndx := instr(l_apex_version, '.');
     l_ndx := l_ndx - 1;
     l_tmp_str := substr(l_apex_version,1,l_ndx);

     l_ver_no := to_number(l_tmp_str);
     
     if (l_ver_no >= 5) or (substr(l_apex_version,1,4) = ('4.2.'))  then
        for c1 in (select table_name from all_tables where owner=l_apex_schema and table_name='WWV_FLOW_RT$MODULES')
        loop
          execute immediate c_grant_select || l_apex_schema || '.' || c1.table_name || c_to_user;
          dbms_output.put_line(c_grant_select || l_apex_schema || '.' || c1.table_name || c_to_user);
        end loop;
        for c1 in (select view_name from all_views where owner=l_apex_schema and view_name='WWV_FLOW_POOL_CONFIG')
        loop
          execute immediate c_grant_select || l_apex_schema || '.' || c1.view_name || c_to_user;
          dbms_output.put_line(c_grant_select || l_apex_schema || '.' || c1.view_name || c_to_user);
        end loop;
     end if;   
   end if;
end;
/
```

The Oracle REST Data Services contains a script, ords_installer_privileges.sql which is located in the scripts/installer folder. The script provides the assigned database user the privileges to install, upgrade, repair, and uninstall ORDS in Oracle Database.
Perform the following steps:

Using SQLcl or SQL*Plus, connect to the Oracle Database instance. You must have a Database account with appropriate privileges for installing ORDS.
    Execute the following script providing the database user:

SQL> @/path/to/scripts/installer/ords_installer_privileges.sql exampleuser
    SQL> exit

You must use the specified database user to install, upgrade, repair, and uninstall ORDS.

> [Return to the Guide](./1-ords-installation-checklist.md#1.2userrequirements)

#### Review Privileges

When the ORDS Installer Privileges script is used, a user is granted equal privileges to install, upgrade, repair, and uninstall ORDS for either/both:

- Oracle Pluggable Database<sup>1</sup>
- Oracle 11g 

<sup>1</sup>Learn about [PDBs](https://docs.oracle.com/en/database/oracle/oracle-database/21/cncpt/introduction-to-oracle-database.html#GUID-ED16D715-761B-4F8B-8503-BC058E216D2F)

> [Return to the Guide](./1-ords-installation-checklist.md#1.2userrequirements)


## 1.3 About the ORDS Command Line tool

### About the ORDS Command Line tool

Beginning in ORDS release 22.1.0 an ORDS Command-Line Interface is included for installation and configuration. This command line interface can be used to:

- Create, update, and list ORDS configurations
- Add additional database pools to your configuration installation/upgrade
- Repair, or uninstall ORDS in the database
- Run ORDS in standalone mode

The preceding functions can be accomplished interactively through prompts, or run silently (non-interactively) using the ORDS commands.

### Basic syntax

Execute a command:

```(shell)
ords <command>
```

Review help and details of a command:

```(shell)
ords <command> --help
```

Review help and details of a command's sub-command:

```(shell)
ords <command> <sub-command> --help
```

### Accessing the ORDS Command Line tool help

The online help provides information about the commands along with the available options and arguments. To show the list of ORDS commands, execute the following command:

```
ords --help
```

![ords-help-command-line-syntax-example](./images/ords-help-command-line-syntax-example.png " ")
*ORDS --help*

To show details and additional help related to an ORDS command, specify the ORDS command followed by `--help`. Two examples can be seen here:

![ords-config-help-example](./images/ords-config-help-example.png " ")
*ORDS config --help*

![ords-extract-help-example](./images/ords-extract-help-example.png " ")
*ORDS extract --help*

You'll notice "sub-commands" in each of the main commands. For additional details, `--help` after the sub-command; as can be seen here:

![ords-config-get-help-example](./images/ords-config-get-help-example.png " ")
*ORDS --help sub-command*

> [Return to the Guide](./1-ords-installation-checklist.md#1.3commandlinetool " ")

### 1.4.1 Option 1: Zip file

This section includes scripts that are included in the ORDS zip file. They include an installer script as well as several ORDS migration scripts.

#### ords_installer_privileges.sql

```sql
Rem  Copyright (c) Oracle Corporation 2014. All Rights Reserved.
Rem
Rem    NAME
Rem      ords_installer_privileges.sql
Rem
Rem    DESCRIPTION
Rem      Provides privileges required to install, upgrade, validate and uninstall 
Rem      ORDS schema, ORDS proxy user and related database objects.
Rem
Rem    NOTES
Rem      This script includes privileges to packages and views that are normally granted PUBLIC 
Rem      because these privileges may be revoked from PUBLIC.
Rem   
Rem
Rem    ARGUMENT:
Rem      1  : ADMINUSER - The database user that will be granted the privilege
Rem
Rem    REQUIREMENTS
Rem      Oracle Database Release 11.1 or later
Rem
Rem    MODIFIED   (MM/DD/YYYY)
Rem      epaglina  09/25/2019  Grant SELECT object privilege if DB version 12.1.0.1.
Rem      epaglina  05/22/2019  Created.
Rem

set define '^'
set serveroutput on
set termout on

define ADMINUSER = '^1'

--
-- System privileges
--
grant alter any table                   to ^ADMINUSER;
grant alter user                        to ^ADMINUSER with admin option;
grant comment any table                 to ^ADMINUSER;
grant create any context                to ^ADMINUSER;
grant create any index                  to ^ADMINUSER;
grant create any job                    to ^ADMINUSER;
grant create any procedure              to ^ADMINUSER;
grant create any sequence               to ^ADMINUSER;
grant create any synonym                to ^ADMINUSER;
grant create any table                  to ^ADMINUSER;
grant create any trigger                to ^ADMINUSER with admin option;
grant create any type                   to ^ADMINUSER;
grant create any view                   to ^ADMINUSER;
grant create job                        to ^ADMINUSER with admin option;
grant create public synonym             to ^ADMINUSER with admin option;
grant create role                       to ^ADMINUSER;
grant create session                    to ^ADMINUSER with admin option;
grant create synonym                    to ^ADMINUSER with admin option;
grant create user                       to ^ADMINUSER;
grant create view                       to ^ADMINUSER with admin option;
grant delete any table                  to ^ADMINUSER;
grant drop any context                  to ^ADMINUSER;
grant drop any role                     to ^ADMINUSER;
grant drop any table                    to ^ADMINUSER;
grant drop any type                     to ^ADMINUSER;
grant drop any synonym                  to ^ADMINUSER;
grant drop public synonym               to ^ADMINUSER with admin option;
grant drop user                         to ^ADMINUSER;
grant execute any procedure             to ^ADMINUSER;
grant execute any type                  to ^ADMINUSER;
grant grant any object privilege        to ^ADMINUSER;
grant insert any table                  to ^ADMINUSER;
grant select any table                  to ^ADMINUSER;
grant update any table                  to ^ADMINUSER;

declare
  c_grant_set_con constant varchar2(255)  := 'grant set container to ' || dbms_assert.enquote_name('^ADMINUSER')
                                           || ' with admin option';
begin
  -- Only for Oracle DB 12c and later
  if sys.dbms_db_version.VERSION >= 12 then
    dbms_output.put_line(c_grant_set_con);
    execute immediate c_grant_set_con;
  end if;
end;
/

--
-- Object privileges with grant option
--
grant execute on sys.dbms_assert        to ^ADMINUSER with grant option;
grant execute on sys.dbms_crypto        to ^ADMINUSER with grant option;
grant execute on sys.dbms_lob           to ^ADMINUSER with grant option;
grant execute on sys.dbms_metadata      to ^ADMINUSER with grant option;
grant execute on sys.dbms_output        to ^ADMINUSER with grant option;
grant execute on sys.dbms_scheduler     to ^ADMINUSER with grant option;
grant execute on sys.dbms_session       to ^ADMINUSER with grant option;
grant execute on sys.dbms_utility       to ^ADMINUSER with grant option;
grant execute on sys.dbms_sql           to ^ADMINUSER with grant option;
grant execute on sys.default_job_class  to ^ADMINUSER with grant option;
grant execute on sys.htp                to ^ADMINUSER with grant option;
grant execute on sys.owa                to ^ADMINUSER with grant option;
grant execute on sys.wpiutl             to ^ADMINUSER with grant option;
grant execute on sys.wpg_docload        to ^ADMINUSER with grant option;

grant select on sys.user_cons_columns   to ^ADMINUSER with grant option;
grant select on sys.user_constraints    to ^ADMINUSER with grant option;
grant select on sys.user_objects        to ^ADMINUSER with grant option;
grant select on sys.user_procedures     to ^ADMINUSER with grant option;
grant select on sys.user_tab_columns    to ^ADMINUSER with grant option;
grant select on sys.user_tables         to ^ADMINUSER with grant option;
grant select on sys.user_views          to ^ADMINUSER with grant option;

--
-- Object privileges
--

-- For Oracle DB 12.1.0.2 and later, grant READ.  Otherwise, grant SELECT.
declare
 type obj_name_list is table of dba_tab_privs.table_name%TYPE;
  list1 obj_name_list := obj_name_list(
                                      'CDB_SERVICES',
                                      'CDB_TABLESPACES',
                                      'DBA_ROLES',
                                      'DBA_SYNONYMS',
                                      'DBA_TABLESPACES',
                                      'DBA_TAB_COLS',
                                      'DBA_TAB_PRIVS',
                                      'DBA_TEMP_FILES',
                                      'PROXY_USERS',
                                      'V_$CONTAINERS',
                                      'V_$DATABASE',
                                      'V_$LISTENER_NETWORK',
                                      'V_$PARAMETER'
                                      );
  -- Include the "with grant option"
  list2 obj_name_list := obj_name_list(
                                      'DBA_OBJECTS',
                                      'DBA_REGISTRY',
                                      'DBA_ROLE_PRIVS',
                                      'DBA_TAB_COLUMNS',
                                      'DBA_USERS',
                                      'SESSION_PRIVS'
                                       );
                                                                           
  c_grant_read constant varchar2(100)  := 'grant read on sys.';
  c_grant_select constant varchar2(100):= 'grant select on sys.';
  c_user_grant constant varchar2(255)  := ' to ' || dbms_assert.enquote_name('^ADMINUSER');
  c_grant_opt constant varchar2(100)   := ' with grant option';
  
  l_use_read boolean          := FALSE;
  l_prod_version varchar2(20) := '';

begin
  if sys.dbms_db_version.VERSION > 12 then
    l_use_read := TRUE;
  elsif sys.dbms_db_version.VERSION = 12 then
    begin
      select version into l_prod_version from sys.v$instance where version like '12.1.0.1.%';
    exception
      when NO_DATA_FOUND then
        -- 12.1.0.2 or later
        l_use_read := TRUE;
      when others then
        null;
    end;
  end if;

  for i in list1.first .. list1.last loop
    if l_use_read then
        -- 12c and later use the READ privilege
      dbms_output.put_line( c_grant_read || list1(i) || c_user_grant);
      execute immediate c_grant_read || list1(i) || c_user_grant;
    elsif (sys.dbms_db_version.VERSION = 12) or
          (sys.dbms_db_version.VERSION = 11 and list1(i) <> 'V_$CONTAINERS') then
      dbms_output.put_line(c_grant_select || list1(i) || c_user_grant);
      execute immediate c_grant_select || list1(i) || c_user_grant;
    end if;
  end loop;
  
  for i in list2.first .. list2.last loop
    if l_use_read then
        -- 12c and later use the READ privilege
      dbms_output.put_line( c_grant_read || list2(i) || c_user_grant || c_grant_opt);
      execute immediate c_grant_read || list2(i) || c_user_grant || c_grant_opt;
    else
      dbms_output.put_line(c_grant_select || list2(i) || c_user_grant || c_grant_opt);
      execute immediate c_grant_select || list2(i) || c_user_grant || c_grant_opt;
    end if;
  end loop;
  
  -- Grant to check if ORDS application is installed in the Application Container
  if (sys.dbms_db_version.version > 12) or (sys.dbms_db_version.version = 12 and sys.dbms_db_version.release > 1) then
    execute immediate c_grant_read || 'DBA_APPLICATIONS' || c_user_grant;
  end if;  
end;
/

-- APEX Support
declare
  c_sel_stmt     constant varchar2(400) := 'select version, schema, status from sys.dba_registry where comp_id = ''APEX''';
  c_grant_select constant varchar2(100) := 'grant select on ';
  c_to_user      constant varchar2(400) := ' to ' || dbms_assert.enquote_name('^ADMINUSER') || ' with grant option';
  l_apex_schema  varchar2(255) := null;
  l_apex_version   varchar2(100) := '';
  l_status         varchar2(100) := null;
  l_tmp_str        varchar2(100) := null;
  l_ver_no         number;
  l_ndx            number;
  
begin
  begin
      execute immediate c_sel_stmt into l_apex_version, l_apex_schema, l_status;
  exception
     when no_data_found then
        null;  -- APEX doesn't exist
  end;
   
  if (l_status is not null) and (l_status = 'VALID') and
      (l_apex_version is not null) and (l_apex_schema is not null) then
   
     l_ndx := instr(l_apex_version, '.');
     l_ndx := l_ndx - 1;
     l_tmp_str := substr(l_apex_version,1,l_ndx);

     l_ver_no := to_number(l_tmp_str);
     
     if (l_ver_no >= 5) or (substr(l_apex_version,1,4) = ('4.2.'))  then
        for c1 in (select table_name from all_tables where owner=l_apex_schema and table_name='WWV_FLOW_RT$MODULES')
        loop
          execute immediate c_grant_select || l_apex_schema || '.' || c1.table_name || c_to_user;
          dbms_output.put_line(c_grant_select || l_apex_schema || '.' || c1.table_name || c_to_user);
        end loop;
        for c1 in (select view_name from all_views where owner=l_apex_schema and view_name='WWV_FLOW_POOL_CONFIG')
        loop
          execute immediate c_grant_select || l_apex_schema || '.' || c1.view_name || c_to_user;
          dbms_output.put_line(c_grant_select || l_apex_schema || '.' || c1.view_name || c_to_user);
        end loop;
     end if;   
   end if;
end;
/
```

#### ords_manual_migrate_workspace.sql

```sql
Rem  Copyright (c) Oracle Corporation 2014. All Rights Reserved.
Rem
Rem    NAME
Rem      ords_manual_migrate_workspace.sql
Rem
Rem    DESCRIPTION
Rem      This script performs a manual migration for Application Express (APEX) Workspace 
Rem      Restful Services to Oracle REST Data Services (ORDS).
Rem
Rem    NOTES
Rem      Assumes user with SYSDBA privilege is connected.
Rem
Rem    REQUIREMENTS
Rem      - Oracle Database 11.1 or later
Rem      - Application Express 4.2.x onwards
Rem
Rem    Arguments:
Rem      1  : Path of log file (include the forward slash at the end)
Rem
Rem    Example:
Rem      sqlplus "sys as sysdba" @ords_manual_migrate_workspace d:/log/scripts/ A_WORKSPACE
Rem
Rem
Rem    MODIFIED    (MM/DD/YYYY)
Rem     dwhittin    02/11/2022 Created.
Rem
Rem

set serveroutput on
timing start "ORDS Migration"

set verify off
set termout off
spool off

set define '^'
set termout on

define LOGFOLDER    = '^1'
define WORKSPACE    = '^2'

whenever sqlerror exit

column logfilename new_val ORDSLOGFILE
select '^LOGFOLDER' || 'ordsmigrate_' || to_char(sysdate,'YYYY-MM-DD_HH24_MI_SS') || '.log' as logfilename from sys.dual;
spool ^ORDSLOGFILE


prompt ******************************************************
prompt * INFO: Oracle REST Data Services (ORDS) Migration.
prompt ******************************************************

prompt * INFO: Migrating APEX Restful Services data to ORDS
@@ords_migrate_workspace_rest.sql ^WORKSPACE

commit;

prompt
prompt *********************************************************
prompt INFO: Completed Oracle REST Data Services Migration.
timing stop
prompt *********************************************************

spool off

exit
```

#### ords_manual_migrate

```sql
Rem  Copyright (c) Oracle Corporation 2014. All Rights Reserved.
Rem
Rem    NAME
Rem      ords_manual_migrate.sql
Rem
Rem    DESCRIPTION
Rem      Manual migration for the Oracle REST Data Services (ORDS).
Rem
Rem    NOTES
Rem      Assumes user with SYSDBA privilege is connected.
Rem
Rem    REQUIREMENTS
Rem      - Oracle Database 11.1 or later
Rem
Rem    Arguments:
Rem      1  : Path of log file (include the forward slash at the end)
Rem
Rem    Example:
Rem      sqlplus "sys as sysdba" @ords_manual_migrate d:/log/scripts/
Rem
Rem
Rem    MODIFIED    (MM/DD/YYYY)
Rem     epaglina    07/25/2014 Created.
Rem
Rem

set serveroutput on
timing start "ORDS Migration"

set verify off
set termout off
spool off

set define '^'
set termout on

define LOGFOLDER    = '^1'

whenever sqlerror exit

column logfilename new_val ORDSLOGFILE
select '^LOGFOLDER' || 'ordsmigrate_' || to_char(sysdate,'YYYY-MM-DD_HH24_MI_SS') || '.log' as logfilename from sys.dual;
spool ^ORDSLOGFILE


prompt ******************************************************
prompt * INFO: Oracle REST Data Services (ORDS) Migration.
prompt ******************************************************

prompt * INFO: Migrating APEX Restful Services data to ORDS
@@ords_migrate_apex_rest.sql

commit;

prompt
prompt *********************************************************
prompt INFO: Completed Oracle REST Data Services Migration.
timing stop
prompt *********************************************************

spool off

exit
```

#### ords_migrate_apex_rest.sql

```sql
Rem  Copyright (c) Oracle Corporation 2014. All Rights Reserved.
Rem
Rem    NAME
Rem      ords_migrate_apex_rest.sql
Rem
Rem    DESCRIPTION
Rem      This script migrates Application Express RESTful Services data 
Rem      (from release 4.2.x or later) to Oracle REST Data Services (ORDS).    
Rem      Do not invoke this script directly.  
Rem      If you are doing a manual migration, use ords_manual_migrate.sql
Rem
Rem    NOTES
Rem      Assumes user with SYSDBA privilege is connected.
Rem
Rem    REQUIREMENTS
Rem      - Oracle Database 11.1 or later
Rem      - Application Express 4.2.x onwards
Rem
Rem    Arguments:
Rem      None
Rem
Rem    MODIFIED    (MM/DD/YYYY)
Rem     epaglina    07/25/2014 - Created.
Rem
Rem

--set serveroutput on

set autocommit off

whenever sqlerror exit sql.sqlcode rollback

begin
  sys.dbms_output.put_line('INFO: ' || to_char(sysdate,'HH24:MI:SS') || ' Migrating APEX RESTful Services definitions to Oracle REST Data Services.');
    ords_metadata.ords_migrate.migrate_apex_restful_services;
  sys.dbms_output.put_line('INFO: ' || to_char(sysdate,'HH24:MI:SS') || ' Completed migrating APEX RESTful Services definitions.');
end;
/
```

#### ords_migrate_report

```sql
Rem  Copyright (c) Oracle Corporation 2014. All Rights Reserved.
Rem
Rem    NAME
Rem      ords_migrate_report.sql
Rem
Rem    DESCRIPTION
Rem      This script reports on Application Express (APEX) Workspace Restful Services
Rem      not yet migrated to Oracle REST Data Services (ORDS).
Rem
Rem    NOTES
Rem      Assumes user with SYSDBA privilege is connected.
Rem
Rem    REQUIREMENTS
Rem      - Oracle Database 11.1 or later
Rem      - Application Express 4.2.x onwards
Rem      - select any table privilege
Rem
Rem    Arguments:
Rem      None
Rem
Rem    MODIFIED    (MM/DD/YYYY)
Rem     dwhittin    02/11/2022 - Created.
Rem
Rem

set termout off
set autocommit off
set verify off
set define '^'
set serveroutput off

whenever sqlerror exit sql.sqlcode rollback

COLUMN :v_apex_installed NEW_VALUE ORDS_APEX_INSTALLED NOPRINT
VARIABLE v_apex_installed VARCHAR2(2000)
COLUMN :v_apex_modules NEW_VALUE ORDS_APEX_MODULES NOPRINT
VARIABLE v_apex_modules VARCHAR2(2000)

-- Lookup APEX schema name and version
declare
  l_schema  VARCHAR(255);
  l_version VARCHAR(255);
  l_status  VARCHAR(255);
  l_ver_no  NUMBER;

  l_migrate_modules_1 VARCHAR2(255) := 
    '
      c.short_name workspace, 
      nvl2(w.schema_id,''YES'',''NO'') migrated,
      count(m.name) module_count
    from 
    ';
  
   l_migrate_modules_2 VARCHAR(500) :=
    '
       ords_metadata.ords_workspace_schemas w
    where 
          c.provisioning_company_id NOT IN (10,11,12) 
      and m.security_group_id = w.workspace_id(+) 
      and m.name NOT IN (''oracle.apex.friendly_url'',''oracle.example.hr'') 
      and m.security_group_id = c.provisioning_company_id 
    group by c.short_name, w.schema_id
    order by migrated, workspace
    ';

  l_null_query VARCHAR2(255) := '''no rows selected'' workspace, null migrated, null modules from dual';
begin
  begin
    l_schema := ords_metadata.ords_migrate.get_apex_schema(
                        p_version => l_version,
                        p_status  => l_status);

   if l_schema is not null then
     if l_version is not null then
       l_ver_no  := to_number(substr(l_version,1, instr(l_version, '.') - 1));

       if l_ver_no < 5 and l_version NOT LIKE '4.2.%' then
         l_status := 'NOT SUPPORTED';
       end if;
     end if;
   else
     l_status := 'NOT AVAILABLE';
   end if;
  exception
    when others then
       l_schema := SQLERRM;
       l_version := SQLCODE;
       l_status := 'ERROR';
  end;

  :v_apex_installed := sys.dbms_assert.enquote_literal(l_schema)  || ' apex_schema, ' ||
                       'nvl(' || sys.dbms_assert.enquote_literal(l_version) || ',''UNKNOWN'')' || ' apex_version, ' ||
                       'nvl(' || sys.dbms_assert.enquote_literal(l_status) || ',''UNKNOWN'')' || ' apex_status from dual';

  if l_status IS NOT NULL AND l_status NOT IN ('VALID') then
    :v_apex_modules := l_null_query;
  else
    :v_apex_modules := l_migrate_modules_1 ||
                       sys.dbms_assert.schema_name(l_schema) || '.wwv_flow_companies c, ' ||
                       sys.dbms_assert.schema_name(l_schema) || '.wwv_flow_rt$modules m, ' ||
                       l_migrate_modules_2;
  end if;
  
end;
/

select :v_apex_installed from dual;
select :v_apex_modules   from dual;

COLUMN workspace      HEADING 'WORKSPACE NAME'
COLUMN migrated       HEADING 'MIGRATED' 
COLUMN module_count   HEADING 'MODULES' 
COLUMN workspace      format   a63
COLUMN migrated       format   a8
COLUMN module_count   format   999999

COLUMN apex_schema    HEADING 'APEX SCHEMA'
COLUMN apex_version   HEADING 'APEX VERSION' 
COLUMN apex_status    HEADING 'APEX STATUS' 
COLUMN apex_schema    format    a48
COLUMN apex_version   format    a15
COLUMN apex_status    format    a15

set termout on

select ^ORDS_APEX_INSTALLED;

select ^ORDS_APEX_MODULES;
```

#### ords_migrate_workspace_rest.sql

```sql
Rem  Copyright (c) Oracle Corporation 2014. All Rights Reserved.
Rem
Rem    NAME
Rem      ords_migrate_workspace_rest.sql
Rem
Rem    DESCRIPTION
Rem      This script migrates Application Express (APEX) Workspace Restful Services to
Rem      Oracle REST Data Services (ORDS).
Rem      Do not invoke this script directly.  
Rem      If you are doing a manual migration, use ords_manual_migrate_workspace.sql
Rem
Rem    NOTES
Rem      Assumes user with SYSDBA privilege is connected.
Rem
Rem    REQUIREMENTS
Rem      - Oracle Database 11.1 or later
Rem      - Application Express 4.2.x onwards
Rem
Rem    Arguments:
Rem      None
Rem
Rem    MODIFIED    (MM/DD/YYYY)
Rem     dwhittin    02/11/2022 - Created.
Rem
Rem

--set serveroutput on

set autocommit off
set verify off
set termout off
set define '^'
set termout on

define WORKSPACE    = '^1'

whenever sqlerror exit sql.sqlcode rollback

begin
  sys.dbms_output.put_line('INFO: ' || to_char(sysdate,'HH24:MI:SS') || ' Migrating APEX RESTful Services definitions to Oracle REST Data Services.');
    ords_metadata.ords_migrate.migrate_apex_workspace_rest(p_workspace_name => '^WORKSPACE');
  sys.dbms_output.put_line('INFO: ' || to_char(sysdate,'HH24:MI:SS') || ' Completed migrating APEX RESTful Services definitions.');
end;
/
```




## 2.1 Java EE Application Servers

