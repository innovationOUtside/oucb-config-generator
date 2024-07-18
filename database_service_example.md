# Database Service Example

The `container-builder` is capable of installing applications that run a services, and, if so configured, ensuring that those services are started on starting the container.

Defining a service via the `services` configuration option also ensure that the user has permissions to `start`, `stop` and `restart` the service.

TO DO - specify sudo config explicitly

## Installing a PostgreSQL Database

To minimally run a PostgreSQL database service inside a VCE built using `container-builder`, we need to install the database and modify a databse server configuration setting.

TO DO

```yaml
packages:
  apt:
    deploy:
    - postgresql
  pip:
    user:
      - jupysql
      - psycopg2-binary
      - pgspecial
      - SQLAlchemy
      - schemadisplay-magic>=0.0.7
scripts:
  - stage: deploy
    commands:
      - sed -e "s/[#]\?listen_addresses = .*/listen_addresses = '*'/g" -i "/etc/postgresql/$PG_VERSION/main/postgresql.conf"
  
services:
  - postgresql
environment:
  - name: PG_VERSION
    value: "15"
  - name: PGDATA
    value: /var/lib/postgresql/$PG_VERSION/main
  - name: POSTGRES_USER
    value: postgres
  - name: POSTGRES_PASSWORD
    value: postgres
  - name: POSTGRES_DB
    value: oudb
  - name: PLOOMBER_STATS_ENABLED
    value: "false"
  - name: PLOOMBER_VERSION_CHECK_DISABLED
    value: "false"
```

## Installing a MongoDB Database

TO DO

To minimally run a MongoDB database service inside a VCE built using `container-builder`, we need to install the database and provide in an appropriate configuration setting file. __The below example requires some external config files to be available.__

```yaml
sources:
  apt:
    - name: mongodb
      key_url: https://www.mongodb.org/static/pgp/server-7.0.asc
      dearmor: True
      deb:
        url: https://repo.mongodb.org/apt/ubuntu
        distribution: jammy/mongodb-org/7.0
        component: multiverse
packages:
  apt:
    deploy:
      - mongodb-org
  pip:
    user:
      - pymongo
content:
  - source: ./db_setup/mongodb-org/mongod
    target: /etc/init.d/mongod
    overwrite: always
  - source: ./db_setup/mongodb-org/mongod.conf
    target: /etc/mongod.conf
    overwrite: always
scripts:
  - stage: deploy
    commands:
      - chmod ugo+rx /etc/init.d/mongod
      - cp -p /etc/mongod.conf /etc/ouseful/mongod.conf
      - chmod u-w /etc/ouseful/mongod.conf
services:
  - mongod
environment:
  - name: MONGO_DB_PATH
    value: /var/db/data/mongo
```


```bash
#! /bin/sh

# Location: ./db_setup/mongodb-org/mongod
# Via: https://github.com/nerdyworm/mongodb_init_d/blob/master/mongodb

### BEGIN INIT INFO
# Provides:          mongod
# Required-Start:    $all
# Required-Stop:     $all
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: starts the mongodb data-store
# Description:       starts mongodb using start-stop-daemon
### END INIT INFO

PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
DAEMON=/usr/bin/mongod
DAEMON_OPTS="-f /etc/mongod.conf"

PIDFILE=/var/run/mongodb.pid
LOGFILE=/var/log/mongod.log
NAME=mongod
DESC=mongod

test -x $DAEMON || exit 0

#set -e

case "$1" in
  start)
        echo -n "Starting $DESC: "
        start-stop-daemon --pidfile $PIDFILE --make-pidfile --start --exec $DAEMON -- $DAEMON_OPTS -- run >> $LOGFILE&
        echo "$NAME."
        ;;
  stop)
        echo -n "Stopping $DESC: "
        start-stop-daemon --stop --quiet --pidfile $PIDFILE
        rm $PIDFILE
        echo "$NAME."
        ;;
  restart|force-reload)
        echo -n "Restarting $DESC: "
        start-stop-daemon --quiet --pidfile $PIDFILE --exec $DAEMON --stop
        sleep 1
        start-stop-daemon --quiet --pidfile $PIDFILE --start --exec $DAEMON -- $DAEMON_OPTS  -- run >> $LOGFILE&
        echo "$NAME."
        ;;
  reload)
      echo -n "Reloading $DESC configuration: "
      start-stop-daemon --stop --signal HUP --quiet --pidfile $PIDFILE --exec $DAEMON
      echo "$NAME."
      ;;
  *)
        N=/etc/init.d/$NAME
        echo "Usage: $N {start|stop|restart|force-reload}" >&2
        exit 1
        ;;
esac

exit 0
```

```yaml
# Location: ./db_setup/mongodb-org/mongod.conf

# for documentation of all options, see:
#   http://docs.mongodb.org/manual/reference/configuration-options/

# Where and how to store data.
storage:
  dbPath: /var/db/data/mongo
#  engine:
#  wiredTiger:

# where to write logging data.
systemLog:
  destination: file
  logAppend: true
  path: /var/log/mongodb/mongod.log

# network interfaces
net:
  port: 27017
  bindIp: 127.0.0.1
  # For external connections,
  # maybe replace with less secure: 0.0.0.0

setParameter:
   enableLocalhostAuthBypass: true

# how the process runs
processManagement:
  timeZoneInfo: /usr/share/zoneinfo

#security:

#operationProfiling:

#replication:

#sharding:

## Enterprise-Only Options:

#auditLog:

#snmp:

```
