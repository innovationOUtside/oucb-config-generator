# Seeded Database Example

If we have installed a database into a `container-builder` built container, we can seed the database during the deployment. This provides a user with a readymade database environment with  users, databases, tables and data available from the start.

## PostgreSQL

If we have a PostgreSQL environment installed, we can seed the database using the following recipe.

*Note that this requires access to a local initialisation files, any other necessary data files.*

```yaml
# Copy the initialisation scripts into the container
content:
  # Database service and initialisation scripts
  - source: ./db_setup/init_db
    target: /var/setup/init_db_seed
scripts:
  # During deployment:
  # - set permissions on the initialisation files
  # - ensure the database service is running
  # - run initialisation scripts
  # - stop the database service
  - stage: deploy
    commands:
      - chmod +x /var/setup/init_db_seed/postgres/init_db.sh
      - service postgresql restart
      - runuser -u postgres -- psql postgres -f /var/setup/init_db_seed/postgres/init_db.sql
      - runuser -u postgres -- /var/setup/init_db_seed/postgres/init_db.sh
      - service postgresql stop
```

Example SQL script to create users, databases etc.

```sql
-- Path: ./db_setup/init_db/postgres/init_db.sql
-- Demo PostgreSQL Database initialisation
CREATE USER testuser PASSWORD 'testpass';
CREATE USER tm351 PASSWORD 'tm351';
CREATE USER tm351_student PASSWORD 'tm351_pwd';
CREATE USER tm351admin PASSWORD 'tm351admin' SUPERUSER;

CREATE USER ou PASSWORD 'ou' SUPERUSER;

DROP TABLE IF EXISTS quickdemo CASCADE;
CREATE TABLE quickdemo(id INT, name VARCHAR(20), value INT);
INSERT INTO quickdemo VALUES(1,'This',12);
INSERT INTO quickdemo VALUES(2,'That',345);

ALTER TABLE quickdemo OWNER TO testuser;
```

Example bash script to create databases, etc.

```bash
#!/bin/bash
# Path: ./db_setup/init_db/postgres/init_db.sh

set -eux

#The -O flag below sets the user: createdb -O DBUSER DBNAME
createdb -O testuser testdb

# Add a database for compatibility with pre-20J notebooks
createdb -O tm351 tm351
createdb -O tm351_student tm351_clean
createdb -O tm351_student tm351_hospital

```

# MongoDB

If we have a MongoDB environment installed, we can seed the database by restoring a previously created database using the following recipe.

*Note that this requires access to a database archive file, e.g. in `./db_setup/init_db/mongodb/db.tar.bz2`.*

```yaml
packages:
  apt:
    # Various uncompress tools if we need to unpack datafiles
    deploy:
      - zip
      - p7zip
content:
  # Database service and initialisation scripts
  - source: ./db_setup/init_db
    target: /var/setup/init_db_seed
  # Mongo config
  - source: ./db_setup/mongodb-org/mongod
    target: /etc/init.d/mongod
    overwrite: always
  - source: ./db_setup/mongodb-org/mongod.conf
    target: /etc/mongod.conf
scripts:
  # During deployment:
  # - ensure the data directory is available
  # - set permissions on the initialisation files
  # - prepare data files
  # - ensure the database service is running
  # - restore a database
  # - stop the database service
  - stage: deploy
    commands:
    overwrite: always
      - mkdir -p ${MONGO_DB_PATH}
      - chmod ugo+rx /etc/init.d/mongod
      - cp -p /etc/mongod.conf /etc/ouseful/mongod.conf
      - chmod u-w /etc/ouseful/mongod.conf
      - mkdir -p /var/setup/tmpdatafiles
      - tar xvjf /var/setup/init_db_seed/mongo/small_accidents.tar.bz2 -C /var/setup/tmpdatafiles
      - service mongod restart
      - mongorestore --drop --db accidents /var/setup/tmpdatafiles/small_accidents
      - service mongod stop
 
```
