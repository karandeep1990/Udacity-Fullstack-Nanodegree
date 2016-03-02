rdb-fullstack
=============

Common code for the Relational Databases and Full Stack Fundamentals courses

## What
- scripts written to create a relationsl sql database and run tests against it.
- The test add, remove sample data, check if sql are performing as they should. 
- the test also check if application specific functions perform as they should

## Author
Karandeep Singh

Udacity - template (tests)

##Usage

1) Install Vagrant

2) Install Virtual box

3) Traverse to vagrant folder in shell (cli)

4) run "vagrant up" -> this will download vagrant image, setup synced folders to "/vagrant, install psql and psql cli, install python

5) ssh into vagrant "ssh vagrant" after vagrant image is created

6) cd into vagrant using "cd /vagrant"

7) "ls" to see all files and folders

8) cd into tournament "cd /tournament"

9) run "psql" to launch psql cli

10) run "\i tournament.sql" to import the sql file -> sets up the databases and tables

11) run "python tournament_test.py" to run the tests agains the postgres sql database


*Note* explore the tournament.sql file for database details and tournament.py for sql functions
