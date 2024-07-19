# Persisted Database Example

If a user updates a database in a container built using `container-builder`, the database will, by default, only be persisted within the container instance.

For users running a local VCE, any changes made to the database will continue to be available as long as the user continues to work within the same container. If the user destroys the container instance and creates a new one, the previous changes will be lost unless they took steps to export the database or create a backup file of it.

For users using a hosted VCE, the container instance is ephemeral: a new container instance is typically created for each new user session. To persist any changes to the database, we need relocate the database data directory into the persisted directory path (e.g. on the user's `$HOME` directory path).

For users working with a local VCE instance, database files can be persisted outside of the container by relocating the database data directory to a shared mounted directory path.

The following recipe can be used optionally copy over database files to a location on the user `$HOME` path.

```yaml
content:
  # User db path
  - source: ./db_setup/setup_root_scripts/
    target: /etc/ou_tmp_setup_root
    overwrite: always
  - source: ./db_setup/local_db_path/
    target: /etc/ou_local_db_path
    overwrite: always
  # Hacks
  - source: ./scripts
    target: /etc/ou_scripts
    overwrite: always
scripts:
  - stage: deploy
    commands:
      - mkdir -p /etc/ouseful/

      - cp -p /etc/postgresql/$PG_VERSION/main/postgresql.conf /etc/ouseful/postgresql.conf
      - chmod u-w /etc/ouseful/postgresql.conf

      - cp -p /etc/mongod.conf /etc/ouseful/mongod.conf
      - chmod u-w /etc/ouseful/mongod.conf

      - chmod u+x /etc/ou_tmp_setup_root/local_sudo.sh
      - /etc/ou_tmp_setup_root/local_sudo.sh
      - rm -r /etc/ou_tmp_setup_root

      - touch ./.no_mount

      - chmod -R ugo+r /etc/ouseful/
      - chmod 555 /etc/ou_local_db_path
      - chmod u+x /etc/ou_local_db_path/local_db_path.sh
      - chmod 555 /etc/ou_scripts
      - chmod u+x /etc/ou_scripts/repair_postgres_db_path.sh
      - chmod u+x /etc/ou_scripts/repair_mongo_db_path.sh
      - touch /home/ou/${MODULE_CODE}-${MODULE_PRESENTATION}/.no_mount
      - chown ou:users /home/ou/${MODULE_CODE}-${MODULE_PRESENTATION}/.no_mount

  - stage: startup
    name: 500-initialising-local-db-mount
    # Call the db migration script using sudo, also
    # passing in some environment state
    commands:
      - sudo PG_VERSION=$PG_VERSION LOCAL_HOME=/home/$USER/${MODULE_CODE}-${MODULE_PRESENTATION} /etc/ou_local_db_path/local_db_path.sh

```

We need to set appropriate permissions on the database migration and utility management scripts.

```bash
#!/bin/bash
# Local path: ./db_setup/setup_root_scripts/local_sudo.sh

# Script to copy database files to shared directory
echo "ou ALL=(ALL:ALL) NOPASSWD: /etc/ou_local_db_path/local_db_path.sh" >> /etc/sudoers

# Script to replace PostgresDB settings files with original settings
echo "ou ALL=(ALL:ALL) NOPASSWD: /etc/ou_scripts/repair_postgres_db_path.sh" >> /etc/sudoers

# Allow passage of specified env vars using sudo
echo 'Defaults env_keep += "LOCAL_HOME PG_VERSION"' >> /etc/sudoers

```

The repair scripts ensure permissions are correctly set on config files.

```bash
#!/bin/bash
# Local path: ./scripts/repair_mongo_db_path.sh
cp /etc/ouseful/mongo.conf /etc/mongod.conf
chmod 644 /etc/mongod.conf
```

```bash
#!/bin/bash
# Local path: ./scripts/repair_postgres_db_path.sh
cp /etc/ouseful/postgresql.conf /etc/postgresql/$PG_VERSION/main/postgresql.conf
chmod 644 /etc/postgresql/$PG_VERSION/main/postgresql.conf
```

The migration script will attempt to migrate the databases and update the configuration files in particular circumstances. Users of the local VCE have some control over whether or not the database directories are copied over to a shared mounted home directory.

```bash
#! /bin/bash
# Local path: ./db_setup/local_db_path/local_db_path.sh
# File location: /etc/ou_local_db_path/local_db_path.sh

# The script should be run via sudo, added elsewhere:
# echo "ou ALL=(ALL:ALL) NOPASSWD: /etc/ou_local_db_path/local_db_path.sh" >> /etc/sudoers

# HOSTED VCE:
# We need to run this script at each startup to rewrite the db config files,
# This should also avoid any races in starting the db in expectation of db
# files being in $HOME before any shared directory is mounted
# It also provides a way for students to force the db to work
# in a non-persistent way for each session by creating
# either $HOME/.no_local_db_path or $HOME/.no_mount

# LOCAL VCE:
# If running e.g. via Docker Desktop there should be a literate log of actions taken.

echo "Running local_db_path.sh script"

# Don't bother with this for now...
#exit 0

#LOCAL_HOME=/home/$USER/${MODULE_CODE}-${MODULE_PRESENTATION}

echo "Temporarily stopping database services"
sudo service postgresql stop
sudo service mongod stop

# If required, don't run any more of this script
if [ -f "$LOCAL_HOME/.no_local_db_path" ]; then
    echo "Not running local db copy scripts"
    echo "Starting db services"
    sudo service postgresql restart
    sudo service mongod restart
    exit 0
fi

## DATABASE MIGRATION

echo "Starting database migration to local file area"

# The Mongo and Postgres data directories can be mounted 
# to the persistent storage that is provided by the Open Computing Lab
# or mounted in from the desktop when using the local VCE.
#
# Migration happens if:
#
# - /home/ou/MODULE-PRESENTATION/.no_local_db_path does not exist
# - /home/ou/MODULE-PRESENTATION/.no_mount does not exist
# - /home/ou/MODULE-PRESENTATION/.local_DBTYPE does not exist (for DBTYPE postgres, mongo)
#
# A ~/.no_mount file is created by default on the $HOME path in the original image.
# This will be clobbered if a volume is mounted over /home/ou/MODULE-PRESENTATION/ ;
# this means databases *will* be copied when the container is run in the hosted VCE.
# In the local VCE with a shared directory mounted onto $HOME, databases *will* be
# copied to host unless the user adds a .no_mount file to the directory they mount
# onto $HOME.

# Create a db hidden storage dir
mkdir -p $LOCAL_HOME/.db

if [[ ! -f "$LOCAL_HOME/.no_mount" ]]; then

    #######  PostgreSQL MIGRATION #######

    # Migrate postgres db to local userdir
    if [[ ! -f "$LOCAL_HOME/.local_postgres" ]] ; then

        sudo service postgresql stop

        echo "Copying over postgres database files to $LOCAL_HOME/.db/"

        # We need to give the postgres user sight into the users...
        #usermod -aG users postgres

        # Recursive copy, preserve permissions
        cp -Rp /var/lib/postgresql $LOCAL_HOME/.db/

        # Manual settings
        #chown -R postgres:postgres $LOCAL_HOME/.db/postgresql
        #chmod -R 700 $LOCAL_HOME/.db/postgresql/

        touch $LOCAL_HOME/.local_postgres
        chown ou:users $LOCAL_HOME/.local_postgres
    else
        echo "No need to copy PostgreSQL files over."
    fi

    # If we have a migrated data directory, update the db config file to use it
    if [[ -d "$LOCAL_HOME/.db/postgresql/$PG_VERSION/main" && ! -f "$LOCAL_HOME/.no_local_postgres" ]]; then
        echo "Updating PostgreSQL config file to point to migrated data dir on: $LOCAL_HOME"
        sed -e "s@[#]\?data_directory = .*@data_directory = '$LOCAL_HOME/.db/postgresql/$PG_VERSION/main'@g" -i "/etc/postgresql/$PG_VERSION/main/postgresql.conf"
    else
        echo "Not updating PostgreSQL config file"
    fi

    #######  MongoDB MIGRATION #######

    if [[ ! -f "$LOCAL_HOME/.local_mongo" ]]; then
        echo "Copying over mongo database files to $LOCAL_HOME/.db/"

        LOCALMONGO="$LOCAL_HOME/.db/mongo/"

        # mongo data directory migration
        if [ -f "/var/run/mongodb.pid" ]; then
            sudo service mongod stop
        fi

        mkdir -p $LOCALMONGO
        # Recursive copy, preserving permissions
        cp -Rp /var/db/data/mongo $LOCAL_HOME/.db

        # Check permissions
        #chmod -R u+rw $LOCALMONGO

        touch $LOCAL_HOME/.local_mongo
        chown ou:users $LOCAL_HOME/.local_mongo
    else
        echo "No need to copy MongoDB files over."
    fi

    # If we have a migrated data directory, update the db config file to use it
    if [[ -d "$LOCAL_HOME/.db/mongo" && ! -f "$LOCAL_HOME/.no_local_mongo" ]]; then
        echo "Updating MongoDB config file to point to migrated data dir on: $LOCAL_HOME"
        sed -e "s@[#]\?dbPath: .*@dbPath: $LOCAL_HOME/.db/mongo@g" -i '/etc/mongod.conf'
    else
        echo "Not updating MongoDB config file"
    fi
else
    echo "No mount - not copying database files over."
fi

# Restart the databases
echo "Restart the database services"

sudo service postgresql restart
sudo service mongod restart

```
