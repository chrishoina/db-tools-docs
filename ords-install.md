# ORDS Installation and Configuration Guide

You said something, regarding, you typically wouldn’t be doing dba type work. But shouldn’t we be leveling the playing field? Wouldn’t it make more sense to make everybody a DBA? That way we can get anybody on our database? 

## 1.1 

Needs correct versions of Oracle DB (edition doesn't matter)

Need network connectivity to your database (where ords is going to be installed)
 - Basic connect string
 - TNS file
 - JDBC url

Error message: The ORDS Java 11 and above should say oracle java 11 or 17.

And we need a sys-level connection. And if not, then you can use the provided instructions for allowing a user to do this. 

## 2.1.2

There is some level of configuration required for the app developer, so it makes sense to simplify this process. Having said that, my notes:

For Mac:

We should include instructions for setting global path for the configuration folder.

![configuration-folder](/images/configuration-folder.png)

Maybe we should include guidance on where this configuration folder should live? Also, should we mention, if this is a brand new/first time install, this folder will be empty at the start? Put it someplace safe, where there are other config files. So it isn't accidentally deleted/ a safe spot? Should be separate from bin files (because in case of upgrade, you retain config folder and delete old bin files)

On my Mac I was able to manually add the following line to my .zprofile file:

```(shell)
#ORDS config folder related
export ORDS_CONFIG = “path…”
```

## 2.1.3 Interactive command line interface installation

### 2.1.3.1

> Select the type of installation. Need language surrounding the default option (which is #2)

I imagine here is where you decide between container and plug-able? If so, we don’t make any reference to each. Should we add language either in the interface or documentation? Reasons or use cases for each?

I skipped 2.1.3.2 - .3 (because I unwittingly chose #1 above). Also we don't discuss the reasons for why you might want to choose Option 1 over -2 or -3. Should there be discussion there?

At the very least, a link/links to learn more about Database [Connection] pools. So people can go learn, and then come back.

![install-number](/images/Enter-install-number.png)

Why is there a [2] in the Choose field?

### 2.1.3.4 Database connection type

![database-connection-type](/images/database-connection-type.png)

The language here is different than what is seen in SQLcl. We see "Basic" here, but in SQLcl I know of "Connect Identifier", which can be either:

- Net Service Name
- Easy Connect

Again, it prompts me with "Choose [1]"...how does it know what I want?

### 2.1.3.5 - 2.1.3.12

> These should be "sub-instructions"

I think there should be different instruction "paths" from the database connection step onward. Because these instructions don't appear if you select Choice 1 in the database connection step:

![tns-location-alias-custom-url](/images/tns-location-alias-custom-url.png)

The prompts screw me up. I think it assumes the database is local? Physically, yes. But virtually (assuming a VM or container) it isn't local, correct? So "localhost" is counterintuitive. This could just be me though.

![database-host-port-service-name](/images/database-host-port-service-name.png)

The listen port shows as [1521]. And while yes, this is technically correct (if referring to TNS listener), it doesn't take into account that I've already done the networking for the container. So my local host is exiting port 43073 and entering port 1521 (to container's listener port).

Regarding the Database Service name; at no point am I prompted between a container or plug-able db. If I refer to the container logs, there is actually no mention of a plug-able db.

![container-logs](/images/container-logs.png)

However, after reviewing the ORDS execution, there is a lot of mention of ORCLPDB1

![orclpdb1-for-apex](/images/orclpdb1-for-apex.png)

![orclpdb1-for-core](/images/orclpdb1-for-core.png)

![orclpdb1-for-scheduler](/images/orclpdb1-for-scheduler.png)

Can "database service name" also be called or known as "Global Database Name" or "System Identifier (SID). I feel like there isn't standardization across the industry; should we include a reference so new users know?

### 2.1.3.13

What our docs say: 

![ords-docs-tablespace](/images/ords-docs-tablespace.png)

What we see during installation:

![common-public-user](/images/common-public-user.png)

Then comes the tablespace information on ORDS install:

![choose-tablespace-in-ords](/images/choose-tablespace-in-ords.png)

But this contradicts what the docs say, no? Because I chose to install ORDS in the database, I shouldn't be prompted for table-space names.

Also, there is no mention of the public user step in the docs. And interestingly enough, we do see that the CDB is the seed for the PDB (for the public user)

Finally, at the end of all this, the output a user receives is:

![ords-install-complete](/images/ords-install-complete.png)

However, in a a previous step, I see mention of the ORDS public user and the ords install in the pdb. I don't see this in the docs, and its confusing because it only briefly mentions the PDB: 

![ords-common-user-ords-pdb](/images/ords-common-user-ords-pdb.png)

## Other notes: 

1. This older version of the [ORDS v17 docs](https://docs.oracle.com/database/ords-17/AELIG/installing-REST-data-services.htm#AELIG7217) was somewhat more helpful (at least with the parameters needed):

![parameters-in-ords](/images/paramaters-for-installing-ords.png)

And this is conflicting regarding what is seen in the ords install. The ords install prompts with the `SYSAUX` table-space, but here it recommends to create a new tables-pace for the user ([link](https://docs.oracle.com/cd/A57673_01/DOC/server/doc/SCN73/ch4.htm)):

![background-info-on-tablespaces](/images/background-info-on-tablespaces.png)

Again, here is what I see during ORDS install: 

![choose-tablespace-in-ords-focus](/images/choose-tablespace-in-ords-focus.png)

** THIS SPACE LEFT INTENTIONALLY BLEAK**