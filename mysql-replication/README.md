## Setup

### Install on 2 VM

```shell
sudo apt-get install mysql-server mysql-client
```

### Config on Master VM

Use a single command to auto-detect the master VM's IP address and write the configuration to /etc/mysql/my.cnf:

```sh
MASTER_IP=$(hostname -I | awk '{print $1}')
if [ -z "$MASTER_IP" ]; then
  MASTER_IP=$(ip route get 1 | awk '{print $7; exit}')
fi
if [ -z "$MASTER_IP" ]; then
  MASTER_IP=$(ifconfig | awk '/inet / && $2 !~ /^127\./ {print $2; exit}')
fi

sudo sh -c "cat > /etc/mysql/my.cnf <<EOF
[mysqld]
bind-address = ${MASTER_IP}
server-id = 1
log_bin = /var/log/mysql/mysql-bin.log
binlog_do_db = petdatabase
EOF"
```

```sh
sudo service mysql restart
```

Copy [pet.txt](pet.txt) into `/tmp/pet.txt`

```sh
mysql -u root -p
```

```sh
GRANT REPLICATION SLAVE ON *.* TO 'slave_user'@'%' IDENTIFIED BY 'password';
FLUSH PRIVILEGES;
CREATE DATABSE petdatabase;
USE petdatabase;
CREATE TABLE pet (name VARCHAR(20), owner VARCHAR(20), species VARCHAR(20), sex CHAR(1), birth DATE, death DATE);
SHOW TABLES;
DESCRIBE pet;
LOAD DATA LOCAL INFILE '/tmp/pet.txt' INTO TABLE pet;
SELECT * FROM pet;
# Wait for Question 1
FLUSH TABLES WITH READ LOCK;
SHOW MASTER STATUS;
# Wait for Question 2
EXIT;
```

Export the database file:

```sh
mysqldump -u root -p --opt petdatabase > petdatabase.sql
```

Send dump to the slave machine:

```sh
scp petdatabase.sql username@IP_Slave_Machine:.
# Wait for Question 3
```

### Config on Slave VM

```sh
mysql -u root -p
```

```sh
CREATE DATABASE petdatabase;
EXIT;
```

```sh
mysql -u root -p petdatabase < /path/to/petdatabase.sql
```

```sh
SLAVE_IP=$(hostname -I | awk '{print $1}')
if [ -z "$SLAVE_IP" ]; then
  SLAVE_IP=$(ip route get 1 | awk '{print $7; exit}')
fi
if [ -z "$SLAVE_IP" ]; then
  SLAVE_IP=$(ifconfig | awk '/inet / && $2 !~ /^127\./ {print $2; exit}')
fi

sudo sh -c "cat > /etc/mysql/my.cnf <<EOF
[mysqld]
bind-address = ${SLAVE_IP}
server-id = 2
log_bin = /var/log/mysql/mysql-bin.log
binlog_do_db = petdatabase
EOF"
```

```sh
sudo service mysql restart
```

Realize the replication:

```sh
mysql -u root -p
```

```sh
CHANGE MASTER TO MASTER_HOST='<MASTER_VM_IP>',
MASTER_USER='<MASTER_VM_MYSQL_USERNAME>', MASTER_PASSWORD='MASTER_VM_MYSQL_PASSWORD',
MASTER_LOG_FILE='mysql-bin.log', MASTER_LOG_POS=107;
```

Start slave

```sh
START SLAVE;
SHOW SLAVE STATUS\G
# Wait for Question 4
```

### Test the replication

Now, you can return to the shell window on the Master machine that you left it blocked. Type:

```sh
UNLOCK TABLES;
```

Try to insert new data to database petdatabase:

```sh
INSERT INTO pet VALUES('Puffball','Diane','hamster','f','1999-03-30',NULL);
# Wait for Question 5
```

## Q&A

Question 1: What is the output did you see? Now, try to add another entry to the
table pet in using SQL queries.

Question 2: What is the name of the log file and the position?

Question 3: Have you received this file in Slave machine? What is the path of this
received file in the Slave machine?

Question 4: What is the status information you received? How do you know the
configuration is OK?

Question 5: In the Slave machine, verify if the new inserted data has been
replicated from Master to Slave. Which command did you use?