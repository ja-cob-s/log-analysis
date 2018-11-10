## Log Analysis
Project for the Udacity Full Stack Web Development Nanodegree.

### Introduction
This project simulates an internal reporting tool that queries a large database of a web server and draws business conclusions from the data. The database contains newspaper articles, as well as the web server log for the site. The PostgreSQL database has the following tables:
* The **authors** table contains data on each of the authors of the articles.
* The **articles** tables contains the full text of the articles.
* The **log** table contains a log of every time a user has accessed the site.

##### The project answers these three questions:
1. What are the most popular three articles of all time? 
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors? 

##### The project follows these standards:
* Good SQL coding practices: Each question is answered with a single database query.
* The code conforms to PEP8 style recommendations and is error free.
* The output is presented in clearly formatted plain text.

### Requirements
* [Python 3](https://www.python.org/) (Written in 3.7.0)
* [Vagrant](https://www.vagrantup.com/)
* [VirtualBox](https://www.virtualbox.org/wiki/Downloads)

### Getting Started
* Clone this repository: `https://github.com/ja-cob-s/log-analysis.git`
* Start the virtual machine: Open a console in the directory where vagrant is installed. From the console, use `vagrant up` and then login with `vagrant ssh`
* Download the [data](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) and unzip into the vagrant directory shared with the virtual machine
* Change to the shared vagrant directory: `cd /vagrant`
* Load the database: Use the command `psql -d news -f newsdata.sql;`
* No views are required for these queries, so you are now ready to run the program.
* Run the program: Use the command `python3 newsdata.py`
* Program output should match what is shown in the `output.txt` file.
